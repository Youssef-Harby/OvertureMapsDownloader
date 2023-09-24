import { useEffect } from "react";
import { convertWkbArrayToGeoJson } from "../services/wkbToGeoJsonService";
import { useDatabase } from "../context/Database";

const DuckDBComponent = ({
    sqlCode,
    shouldExecute,
    setShouldExecute,
    setResult,
    setError,
    setQueryTime,
    setConversionTime,
}) => {
    const database = useDatabase();


    useEffect(() => {
        if (!shouldExecute) return;
        let { conn } = database;
        const fetchData = async () => {
            try {
                const startQueryTime = performance.now();
                const data = await conn.query(sqlCode);
                const endQueryTime = performance.now();
                setQueryTime(endQueryTime - startQueryTime);

                const startConversionTime = performance.now();
                const geoJsonData = convertWkbArrayToGeoJson(JSON.parse(data));
                const endConversionTime = performance.now();
                setConversionTime(endConversionTime - startConversionTime);

                setResult(geoJsonData);
                setError(null); // Clear any previous errors
            } catch (e) {
                setError(e.toString());
            } finally {
                setShouldExecute(false); // Reset the flag
            }
        };

        fetchData();
    }, [
        sqlCode,
        shouldExecute,
        setShouldExecute,
        setResult,
        setError,
        setQueryTime,
        setConversionTime,
        database,
    ]);

    return null; // No need to return anything here
};

export default DuckDBComponent;
