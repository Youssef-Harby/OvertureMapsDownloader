import { MapLibreMap, useMap } from '@mapcomponents/react-maplibre';
import { MlGeoJsonLayer } from "@mapcomponents/react-maplibre";
import { useEffect, forwardRef, useImperativeHandle } from 'react';

const MapComponent = forwardRef(({ result, error }, ref) => {
    const mapOptions = {
        zoom: 5,
        style: "https://wms.wheregroup.com/tileserver/style/osm-bright.json",
        center: [31.0, 31.0]
    };

    const mapHook = useMap({ mapId: "map_1" });

    useImperativeHandle(ref, () => ({
        resize: () => {
            mapHook.map?.resize();
        }
    }));

    useEffect(() => {
        if (mapHook.map) {
            mapHook.map.on('load', function () {
                // Trigger a resize event
                mapHook.map.resize();
            });
        }
    }, [mapHook.map]);

    useEffect(() => {
        if (result && result.features && result.features.length > 0) {
            const firstFeature = result.features[0];
            const coordinatesObj = firstFeature.geometry.coordinates;

            // Convert the coordinates object to an array
            const coordinates = [coordinatesObj["0"], coordinatesObj["1"]];

            // Delay the flyTo operation
            setTimeout(() => {
                mapHook.map?.flyTo({
                    center: coordinates,
                    zoom: 10,
                });
            }, 500); // 500 milliseconds delay
        }
    }, [result, error, mapHook.map]);

    return (
        <>
            <MapLibreMap options={mapOptions} mapId="map_1" />
            {result && (
                <MlGeoJsonLayer
                    geojson={result}
                    mapId="map_1"
                />
            )}
        </>
    );
});

MapComponent.displayName = 'MapComponent';

export default MapComponent;
