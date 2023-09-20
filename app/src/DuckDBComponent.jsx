import { useEffect } from 'react';
import { initDatabase } from '../services/duckdb';
import { convertWkbArrayToGeoJson } from '../services/wkbToGeoJsonService';

const DuckDBComponent = ({ sqlCode, shouldExecute, setShouldExecute, setResult, setError, setQueryTime, setConversionTime }) => {
    useEffect(() => {
        if (!shouldExecute) return;

        let conn, db, worker;

        const fetchData = async () => {
            try {
                const startQueryTime = performance.now();
                ({ conn, db, worker } = await initDatabase(':memory:'));

                const data = await conn.query(sqlCode);
                const endQueryTime = performance.now();
                setQueryTime(endQueryTime - startQueryTime);

                const startConversionTime = performance.now();
                const geoJsonData = convertWkbArrayToGeoJson(JSON.parse(data));
                const endConversionTime = performance.now();
                setConversionTime(endConversionTime - startConversionTime);

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
    }, [sqlCode, shouldExecute, setShouldExecute, setResult, setError, setQueryTime, setConversionTime]);

    return null;  // No need to return anything here
};

export default DuckDBComponent;

