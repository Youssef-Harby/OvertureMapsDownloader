import { useState } from 'react';
import DuckDBComponent from './DuckDBComponent';
import AceEditorComponent from './AceEditorComponent';

function App() {
  const [code, setCode] = useState(`
SELECT 
    id
FROM 
    'https://data.source.coop/cholmes/overture/places-geoparquet-country/AD.parquet'
LIMIT 
    2;
  `);
  const [shouldExecute, setShouldExecute] = useState(false);

  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  const handleExecuteClick = () => {
    setShouldExecute(true);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="text-4xl font-bold mb-4">DuckDB Editor</div>
      <div className="w-full max-w-2xl mb-8">
        <AceEditorComponent initialCode={code} onCodeChange={handleCodeChange} />
      </div>
      <button
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        onClick={handleExecuteClick}
      >
        Run Query
      </button>
      <div className="w-full max-w-2xl">
        <DuckDBComponent sqlCode={code} shouldExecute={shouldExecute} setShouldExecute={setShouldExecute} />
      </div>
    </div>
  );
}

export default App;
