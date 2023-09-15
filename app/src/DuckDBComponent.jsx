import { useEffect } from 'react';
import { initDatabase } from '../services/duckdb';
import { convertWkbArrayToGeoJson } from '../services/wkbToGeoJsonService';

const DuckDBComponent = ({ sqlCode, shouldExecute, setShouldExecute, setResult, setError }) => {
    useEffect(() => {
        if (!shouldExecute) return;

        let conn, db, worker;

        const fetchData = async () => {
            try {
                ({ conn, db, worker } = await initDatabase(':memory:'));

                const data = await conn.query(sqlCode);
                const geoJsonData = convertWkbArrayToGeoJson(JSON.parse(data));

                setResult(geoJsonData);
                setError(null);  // Clear any previous errors
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
    }, [sqlCode, shouldExecute, setShouldExecute, setResult, setError]);

    return null;  // No need to return anything here
};

export default DuckDBComponent;

