import { MapLibreMap } from '@mapcomponents/react-maplibre';
import { MlGeoJsonLayer } from "@mapcomponents/react-maplibre";
import { useEffect } from 'react';

const MapComponent = ({ result, error }) => {
    const mapOptions = {
        zoom: 4,
        style: "https://wms.wheregroup.com/tileserver/style/osm-bright.json",
        center: [7.0851268, 50.73884]
    };

    useEffect(() => {
        console.log("Result from MapComponent.jsx is : ", result);
        console.log("Error from MapComponent.jsx is : ", error);
    }, [result, error]);

    return (
        <>
            <MapLibreMap style={{ width: "100%" }} options={mapOptions} mapId="map_1" />
            {result && (
                <MlGeoJsonLayer
                    geojson={result}
                    mapId="map_1"
                />
            )}
        </>
    );
};

export default MapComponent;
