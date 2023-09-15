import { useState, useEffect } from 'react';
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

  const [shouldExecute, setShouldExecute] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  const handleExecuteClick = () => {
    setShouldExecute(true);
  };

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-grow overflow-y-auto">
        <Splitter
          direction={SplitDirection.Horizontal}
          gutterClassName="!h-[unset] w-2 bg-gray-200 border-none min-h-screen"
        >
          <div className="flex flex-col h-full">
            <AceEditorComponent initialCode={code} onCodeChange={handleCodeChange} />
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mx-4 my-4 rounded"
              onClick={handleExecuteClick}
            >
              Run Query
            </button>
            {error ? (
              <p className="text-red-500">Error: {error}</p>
            ) : (
              <AceEditorComponent initialCode={JSON.stringify(result, null, 2)} readOnly={true} />
            )}
          </div>
          <div className="h-full max-w-full w-full">
            <DuckDBComponent sqlCode={code} shouldExecute={shouldExecute} setShouldExecute={setShouldExecute} setResult={setResult} setError={setError} />
            <MapComponentsProvider>
              <MapComponent result={result} error={error} />
            </MapComponentsProvider>
          </div>
        </Splitter>
      </div>
    </div>
  );
}

export default App;
