import { MapLibreMap, useMap } from '@mapcomponents/react-maplibre';
import { MlGeoJsonLayer } from "@mapcomponents/react-maplibre";
import { useEffect, forwardRef, useImperativeHandle } from 'react';

const MapComponent = forwardRef(({ result, error, onBoundingBoxChange }, ref) => {
    const mapOptions = {
        zoom: 5,
        style: "https://wms.wheregroup.com/tileserver/style/osm-bright.json",
        center: [31.0, 31.0]
    };

    const mapHook = useMap({ mapId: "map_1" });

    useImperativeHandle(ref, () => ({
        resize: () => {
            mapHook.map?.resize();
        },
        getBoundingBox: () => {
            if (mapHook.map) {
                const bounds = mapHook.map.getBounds();
                return {
                    minx: bounds.getWest(),
                    maxx: bounds.getEast(),
                    miny: bounds.getSouth(),
                    maxy: bounds.getNorth(),
                };
            }
            return null;
        }
    }));


    useEffect(() => {
        if (mapHook.map) {
            mapHook.map.on('load', function () {
                // Trigger a resize event
                mapHook.map.resize();
            });
        }

        // Cleanup: remove event listener when component is unmounted or map instance changes
        return () => {
            mapHook.map?.off('moveend');
        };
    }, [mapHook.map, onBoundingBoxChange]);

    useEffect(() => {
        if (result && result.features && result.features.length > 0) {
            const firstFeature = result.features[0];
            let coordinates = [];

            if (firstFeature.geometry.type === 'Point') {
                coordinates = firstFeature.geometry.coordinates;
            } else if (['LineString', 'Polygon', 'MultiPoint', 'MultiLineString', 'MultiPolygon'].includes(firstFeature.geometry.type)) {
                // Extract the first coordinate of the first linear ring for 'Polygon' and 'MultiPolygon',
                // or the first coordinate of the line string for 'LineString' and 'MultiLineString',
                // or the first coordinate for 'MultiPoint'.
                coordinates = firstFeature.geometry.coordinates.flat(2).slice(0, 2);
            }

            if (coordinates.length === 2) {
                setTimeout(() => {
                    mapHook.map?.flyTo({
                        center: coordinates,
                        zoom: 16,
                    });
                }, 500);
            }
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
