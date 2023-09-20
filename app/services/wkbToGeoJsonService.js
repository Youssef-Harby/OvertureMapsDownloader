import { WKBLoader } from '@loaders.gl/wkt';
import { parseSync } from '@loaders.gl/core';

export const convertWkbArrayToGeoJson = (wkbArray) => {
    const features = wkbArray.map((item) => {
        // Convert the WKB geometry to a Uint8Array buffer
        const wkbBuffer = new Uint8Array(item.geometry).buffer;
        console.log(item.geometry);
        console.log(wkbBuffer);

        // Parse the WKB buffer using @loaders.gl/wkt
        const parsedData = parseSync(wkbBuffer, WKBLoader);

        // Extract the positions (coordinates) from the parsed data
        const positions = parsedData.positions.value;

        // Delete the geometry field from the item object
        delete item.geometry;

        // Create the GeoJSON geometry object
        const geoJsonGeometry = {
            type: 'Point', // Replace with the actual geometry type
            coordinates: positions
        };

        // Create the properties object
        const properties = {
            ...item
            // any other key-value pairs you want to add to the properties
        };

        return {
            type: 'Feature',
            properties,
            geometry: geoJsonGeometry
        };
    });

    return {
        type: 'FeatureCollection',
        features
    };
};