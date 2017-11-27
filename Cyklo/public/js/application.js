mapboxgl.accessToken = 'pk.eyJ1IjoiYnJva29saWNrYSIsImEiOiJjaXoyenF1ZmcwMDJpMnhxdGVvZ3g2YXh3In0.QsZbHS7KdM1b_13YrdS-xw';
var map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/kummi/cjaikl41w9z1n2rl0ps2rfv0w', //hosted style id
        center: [18.098340299765397,48.51165243528095], // starting position
        zoom: 10 // starting zoom
});

map.loadImage('/static/js/restaurant.png', function(error, image) {
    if (error) throw error;
    map.addImage('rest', image);
});

map.loadImage('/static/js/phar.png', function(error, image) {
    if (error) throw error;
    map.addImage('phar', image);
});

var layerGroup = [];



$(document).ready(function(){
    $('#One').click(function(){
        var data = {};
            data['distance']=$('#distance').val();
            data['lng']=$('#lng').val();
            data['lat']=$('#lat').val();
        $.ajax({
            url: '/Surroundings',
            type: 'post',
            data: data,
            success: function (e) {
                console.log(JSON.parse(e));
                alert("Done");
                var idcka = String(Math.random());
                layerGroup.push(idcka);
                map.addLayer({
                    "id":  idcka,
                    "type": "line",
                    "source": {
                        "type": "geojson",
                        "data": JSON.parse(e)
                    },
                    "paint": {
                    "line-color": "#FF00BF",
                    "line-width": 5
                }

                });
            }
        });
    });
     $('#Four').click(function(){
        var data = {};
        data['distance']=$('#distance').val();
        data['lng']=$('#lng').val();
        data['lat']=$('#lat').val();
        $.ajax({
            url: '/Pharmacy',
            type: 'post',
            data: data,
            success: function (e) {
                console.log(JSON.parse(e));
                alert("Done");
                var idcka = String(Math.random());
                layerGroup.push(idcka);
                map.addLayer({
                    "id":  idcka,
                    "type": "symbol",
                    "source": {
                        "type": "geojson",
                        "data": JSON.parse(e)
                    },
                    "layout": {
                        "icon-image": "phar",
                        "icon-size": 0.2
                    }

                });
            }
        });
    });
    $('#Three').click(function(){
        var data = {};
        data['distance']=$('#distance').val();
        data['lng']=$('#lng').val();
        data['lat']=$('#lat').val();
        $.ajax({
            url: '/Nearest',
            type: 'post',
            data: data,
            success: function (e) {
                //console.log(JSON.parse(e));
                alert("Done");
                var idcka = String(Math.random());
                layerGroup.push(idcka);
                map.addLayer({
                    "id":  idcka,
                    "type": "line",
                    "source": {
                        "type": "geojson",
                        "data": JSON.parse(e)
                    },
                    "paint": {
                    "line-color": "#00ffff",
                    "line-width": 5
                }

                });
            }
        });
    });

    $('#Five').click(function(){
        var data = {};
        data['distance']=$('#distance').val();
        data['lng']=$('#lng').val();
        data['lat']=$('#lat').val();
        $.ajax({
            url: '/Food',
            type: 'post',
            data: data,
            success: function (e) {
                console.log(e);
                alert("Done");
                var idcka = String(Math.random());
                layerGroup.push(idcka);
                map.addLayer({
                    "id":  idcka,
                    "type": "symbol",
                    "source": {
                        "type": "geojson",
                        "data": JSON.parse(e)
                    },
                    "layout": {
                        "icon-image": "rest",
                        "icon-size": 1
                    }

                });
            }
        });
    });

    $('#Two').click(function(){
        var data = {};
        $.ajax({
            url: '/clear',
            type: 'post',
            data: {},
            success: function (e) {
                //console.log(e);
                layerGroup.forEach(function(e){
                    map.removeLayer(e)
                    layerGroup.shift()
                })
                alert("cleared");

            }
        });
    });
});








map.on('click', function (e) {
      new mapboxgl.Popup().setLngLat(e.lngLat).setHTML(JSON.stringify(e.lngLat)).addTo(map);
      $('#lng').val(e.lngLat.lng);
      $('#lat').val(e.lngLat.lat);



    });
