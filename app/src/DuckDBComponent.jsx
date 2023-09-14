import { useEffect, useState } from 'react';
import { initDatabase } from '../services/duckdb';

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

                console.log(data);
                setResult(data);
            } catch (e) {
                console.error('An error occurred:', e);
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
        <div className="flex flex-col items-center">
            {error ? (
                <p className="text-red-500">Error: {error}</p>
            ) : (
                <p className="text-3xl font-bold underline">Result: {result}</p>
            )}
        </div>
    );
};

export default DuckDBComponent;
