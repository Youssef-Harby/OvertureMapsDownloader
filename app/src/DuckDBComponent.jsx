import { useEffect, useState } from 'react';
import { initDatabase } from '../services/duckdb';
import { convertWkbArrayToGeoJson } from '../services/wkbToGeoJsonService';
import { MapComponentsProvider } from '@mapcomponents/react-maplibre';
import MapComponent from './MapComponent';

const DuckDBComponent = ({ sqlCode, shouldExecute, setShouldExecute }) => {
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!shouldExecute) return;

        let conn, db, worker;

        const fetchData = async () => {
            try {
                ({ conn, db, worker } = await initDatabase(':memory:'));

                const data = await conn.query(sqlCode);
                const geoJsonData = convertWkbArrayToGeoJson(JSON.parse(data));

                setResult(geoJsonData);
            } catch (e) {
                setError(e.toString());
            } finally {
                if (conn) await conn.close();
                if (db) await db.terminate();
                if (worker) worker.terminate();
                setShouldExecute(false);  // Reset the flag
            }
        };

        fetchData();
    }, [sqlCode, shouldExecute, setShouldExecute]);

    return (
        <div>
            {error ? (
                <p className="text-red-500">Error: {error}</p>
            ) : (
                <p className="font-bold underline">Result: {JSON.stringify(result, null, 2)}</p>
            )}
            <MapComponentsProvider>
                <MapComponent result={result} error={error} />
            </MapComponentsProvider>
        </div>
    );
};

export default DuckDBComponent;
