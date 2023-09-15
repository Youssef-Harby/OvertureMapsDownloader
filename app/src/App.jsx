import { useState, useRef } from 'react';
import DuckDBComponent from './DuckDBComponent';
import AceEditorComponent from './AceEditorComponent';
import Splitter, { SplitDirection } from '@devbookhq/splitter';
import { MapComponentsProvider } from '@mapcomponents/react-maplibre';
import MapComponent from './MapComponent';

function App() {
  const [code, setCode] = useState(`
SELECT 
    id,
    geometry
FROM 
    'https://data.source.coop/cholmes/overture/places-geoparquet-country/AD.parquet'
LIMIT 
    2;
  `);
  const [queryTime, setQueryTime] = useState(null);
  const [conversionTime, setConversionTime] = useState(null);
  const [shouldExecute, setShouldExecute] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const mapRef = useRef(null);

  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  const handleExecuteClick = () => {
    setShouldExecute(true);
  };

  const handleResizeFinished = () => {
    mapRef.current?.resize();
  };

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-grow overflow-y-auto">
        <Splitter
          direction={SplitDirection.Horizontal}
          gutterClassName="!h-[unset] w-2 bg-gray-200 border-none min-h-screen"
          onResizeFinished={handleResizeFinished}
        >
          <div className="flex flex-col h-full">
            <AceEditorComponent initialCode={code} onCodeChange={handleCodeChange} />
            <div className="flex items-center space-x-4 mx-4 my-4">
              <button
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                onClick={handleExecuteClick}
              >
                Run Query
              </button>
              <div className='text-green-500'>
                <p>Query Time (parquet): {queryTime ? `${queryTime.toFixed(2)} ms` : 'N/A'}</p>
                <p>Conversion Time (GeoJSON): {conversionTime ? `${conversionTime.toFixed(2)} ms` : 'N/A'}</p>
              </div>
            </div>
            {error ? (
              <p className="text-red-500">Error: {error}</p>
            ) : (
              <AceEditorComponent initialCode={JSON.stringify(result, null, 2)} readOnly={true} />
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
  );
}

export default App;
