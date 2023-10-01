import { WKBLoader } from '@loaders.gl/wkt';
import { parseSync } from '@loaders.gl/core';

export const convertWkbArrayToGeoJson = (wkbArray) => {
    const features = wkbArray.map((item) => {
        const wkbBuffer = new Uint8Array(item.geometry).buffer;
        const parsedData = parseSync(wkbBuffer, WKBLoader);
        const geometryType = parsedData.type;

        let coordinates = [];

        if (['Point'].includes(geometryType)) {
            coordinates = Array.from(parsedData.positions.value);
        } else if (['Polygon', 'LineString', 'MultiLineString', 'MultiPolygon'].includes(geometryType)) {
            const positions = parsedData.positions.value;

            // Assuming positions are flat [x1, y1, x2, y2,...], group them as coordinate pairs [[x1, y1], [x2, y2],...]
            for (let i = 0; i < positions.length; i += 2) {
                coordinates.push([positions[i], positions[i + 1]]);
            }

            if (['Polygon', 'MultiPolygon'].includes(geometryType)) {
                // For 'Polygon' and 'MultiPolygon', coordinates should be wrapped in an additional array to represent linear rings
                coordinates = [coordinates];
            }
        }

        delete item.geometry;

        return {
            type: 'Feature',
            properties: { ...item },
            geometry: { type: geometryType, coordinates }
        };
    });

    return { type: 'FeatureCollection', features };
};
