import { useState, useRef, useEffect } from "react";
import DuckDBComponent from "./DuckDBComponent";
import AceEditorComponent from "./AceEditorComponent";
import Splitter, { SplitDirection } from "@devbookhq/splitter";
import { MapComponentsProvider } from "@mapcomponents/react-maplibre";
import MapComponent from "./MapComponent";
import { DatabaseProvider } from "../context/Database";
import { initDatabase } from "../services/duckdb";

function App() {
  const [database, setDatabase] = useState();
  const [code, setCode] = useState(`
SELECT 
    id,
    geometry
FROM 
    'https://data.source.coop/cholmes/overture/places-geoparquet-country/AD.parquet'
WHERE
    bbox.minx > 1.5862501972418102 
AND bbox.maxx < 1.7887386087803065 
AND bbox.miny > 42.441143243916 
AND bbox.maxy < 42.68483211413101
LIMIT 
    100;

`);
  const [queryTime, setQueryTime] = useState(null);
  const [conversionTime, setConversionTime] = useState(null);
  const [shouldExecute, setShouldExecute] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const mapRef = useRef(null);

  const handleGetBBOXClick = () => {
    const bbox = mapRef.current?.getBoundingBox();
    if (bbox) {
      const bboxFilter = `
bbox.minx > ${bbox.minx} 
AND bbox.maxx < ${bbox.maxx} 
AND bbox.miny > ${bbox.miny} 
AND bbox.maxy < ${bbox.maxy}
`;

      // Regular expression to match the --bbox placeholder or an existing BBOX filter.
      const bboxRegex = /(--bbox|bbox\.minx\s*>\s*-?\d+(\.\d+)?\s*AND\s*bbox\.maxx\s*<\s*-?\d+(\.\d+)?\s*AND\s*bbox\.miny\s*>\s*-?\d+(\.\d+)?\s*AND\s*bbox\.maxy\s*<\s*-?\d+(\.\d+)?)/;

      // Replace the --bbox placeholder or an existing BBOX filter with the new BBOX filter.
      const newCode = code.replace(bboxRegex, bboxFilter.trim());

      setCode(newCode);
    }
  };



  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  const handleExecuteClick = () => {
    setShouldExecute(true);
  };

  const handleResizeFinished = () => {
    mapRef.current?.resize();
  };

  useEffect(() => {
    const bootstrap = async () => {
      const { conn, db, worker } = await initDatabase(":memory:");
      setDatabase({ conn, db, worker });
    };
    bootstrap();
  }, []);

  return (
    <DatabaseProvider
      value={database}
    >
      <div className="flex flex-col h-screen">
        <div className="flex-grow overflow-y-auto">
          <Splitter
            direction={SplitDirection.Horizontal}
            gutterClassName="!h-[unset] w-2 bg-gray-200 border-none min-h-screen"
            onResizeFinished={handleResizeFinished}
          >
            <div className="flex flex-col h-full">
              <AceEditorComponent
                initialCode={code}
                onCodeChange={handleCodeChange}
              />
              <div className="flex items-center space-x-4 mx-4 my-4">
                <button
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                  onClick={handleExecuteClick}
                >
                  Run Query
                </button>
                <button
                  className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                  onClick={handleGetBBOXClick}
                >
                  Get BBOX
                </button>
                <div className="text-green-500">
                  <p>
                    Query Time (parquet):{" "}
                    {queryTime ? `${queryTime.toFixed(2)} ms` : "N/A"}
                  </p>
                  <p>
                    Conversion Time (GeoJSON):{" "}
                    {conversionTime ? `${conversionTime.toFixed(2)} ms` : "N/A"}
                  </p>
                </div>
              </div>
              {error ? (
                <p className="text-red-500">Error: {error}</p>
              ) : (
                <AceEditorComponent
                  initialCode={JSON.stringify(result, null, 2)}
                  readOnly={true}
                />
              )}
            </div>
            <div className="h-full max-w-full w-full">
              <DuckDBComponent
                sqlCode={code}
                shouldExecute={shouldExecute}
                setShouldExecute={setShouldExecute}
                setResult={setResult}
                setError={setError}
                setQueryTime={setQueryTime}
                setConversionTime={setConversionTime}
              />
              <MapComponentsProvider>
                <MapComponent ref={mapRef} result={result} error={error} />
              </MapComponentsProvider>
            </div>
          </Splitter>
        </div>
      </div>
    </DatabaseProvider>
  );
}

export default App;
