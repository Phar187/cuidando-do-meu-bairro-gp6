window.onload = function() {

	function getlocation(coordenadas) {
		if("cep" in coordenadas) {
			return coordenadas['cep'];
		}

		var more_priority = [];
		var less_priority = [];
		var keys = Object.keys(coordenadas);
		$.each(keys, function(index, key) {
			var priorities = ["bairro", "cidade", "comunidade", "conjunto", "distrito", "favela", "jardim",
												"loteamento", "morro", "recanto", "sitio", "subprefeitura", "vila"];

			if($.inArray(key, priorities) != -1) {
			 	less_priority = less_priority.concat(coordenadas[key]);
			 } else {
			 	more_priority = more_priority.concat(coordenadas[key]);
			 }
		});
		if(more_priority.length != 0) {
			return more_priority;
		} else {
			return less_priority;
		}
	}

	function getdescription(entry) {
		var description = 'ID: ' + entry.id +
				'<br>' + entry.descricao +
				'<br>Orçado: ' + entry.orcado +
				'<br>Atualizado: ' + entry.atualizado +
				'<br>Empenhado: ' + entry.empenhado +
				'<br>Liquidado: ' + entry.liquidado +
				'<br>Órgão: ' + entry.orgao +
				'<br>Unidade: ' + entry.unidade +
				'<br>Função: ' + entry.funcao +
				'<br>Subfunção: ' + entry.subfuncao +
				'<br>Programa: ' + entry.programa;
			try {
				description = description + '<br>Despesa: ' + entry.descricao_desp;
			} catch (err) {}
		return description;
	}


	//icones
	var greenIcon = L.icon({
		iconUrl: 'img/verde.png',
		iconSize: [25, 41],
		popupAnchor: [0, -10],
	});
	var blueIcon = L.icon({
		iconUrl: 'img/azul.png',
		iconSize: [25, 41],
		popupAnchor: [0, -10],
	});
	var redIcon = L.icon({
		iconUrl: 'img/vermelho.png',
		iconSize: [25, 41],
		popupAnchor: [0, -10],
	});
	var yellowIcon = L.icon({
		iconUrl: 'img/amarelo.png',
		iconSize: [25, 41],
		popupAnchor: [0, -10],
	});

	function getcolor(entry) {
    a = entry
		if(entry.atualizado == "0,00" && entry.empenhado == "0,00" && entry.liquidado == "0,00") {
			return redIcon;
		} else if(entry.empenhado == "0,00" && entry.liquidado == "0,00") {
			return yellowIcon;
		} else if(entry.liquidado == "0,00") {
			return greenIcon;
		} else {
			return blueIcon;
		}
	}


	var markersArray = [];
	var mapped_list_html = '<table cellspacing="0"><tr><th scope="col" class="nobg">ID</th><th scope="col">Descrição</th><th scope="col">Orçado</th><th scope="col">Atualizado</th><th scope="col">Empenhado</th><th scope="col">Liquidado</th><th scope="col">Órgão</th></tr>';
	var notmapped_list_html = mapped_list_html;
	
	function appendTableEntry(list, entry, rowclass) {
		var html = '<tr>';
		html += '<th scope="row" class="spec' + rowclass +'">' + entry.id + '</th>';
		if(list == 'mapped') {
			html += '<td class="' + rowclass + '">' + '<a onclick="gotoMarker(' + (markersArray.length-1) + ')">' + entry.descricao + '</a></td>';		
		} else {
			html += '<td class="' + rowclass + '">' + entry.descricao + '</td>';
		}
		html += '<td class="' + rowclass + '">' + entry.orcado + '</td>';
		html += '<td class="' + rowclass + '">' + entry.atualizado + '</td>';
		html += '<td class="' + rowclass + '">' + entry.empenhado + '</td>';
		html += '<td class="' + rowclass + '">' + entry.liquidado + '</td>';
		html += '<td class="' + rowclass + '">' + entry.orgao + '</td>';
		html += '</tr>';
		if(list == 'mapped') {
			mapped_list_html += html;
		} else {
			notmapped_list_html += html;
		}
	}

	// USANDO MAPQUEST
	var map = L.map('map-wrapper', {
		layers: MQ.mapLayer(),
		center: [ -23.58098, -46.61293 ],
		zoom: 12
	});

	// USANDO MAPBOX
	//var map = L.map('map-wrapper').setView([-23.58098, -46.61293], 11);
	//L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
	//	maxZoom: 18,
	//	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
	//		'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
	//		'Imagery © <a href="http://mapbox.com">Mapbox</a>',
	//	id: 'andresmrm.j7bc97nk'
	//}).addTo(map);

	var oms = new OverlappingMarkerSpiderfier(map);

	var popup = new L.Popup();
	window.abrirPopup = function (marker) {
		popup.setContent(marker.desc);
		popup.setLatLng(marker.getLatLng());
		map.openPopup(popup);
	}
	oms.addListener('click', window.abrirPopup);

	var corrente = L.layerGroup();
	var capital = L.layerGroup();
	var naoident = L.layerGroup();

	function drawMarkers(data) {
		var mappedRowClass = '', notMappedRowClass = '';
		$.each(data, function(index, entry) {
			if(Object.keys(entry.coordenadas).length != 0) {
				$.each(getlocation(entry.coordenadas), function(index, location) {

					var marker = L.marker([location.localizacoes[0].lat, location.localizacoes[0].lng],{icon: getcolor(entry), title: entry.descricao});
					marker.desc = getdescription(entry);
			try {
				var codigo = entry.descricao_desp[0];
				if (codigo == "3") {
					corrente.addLayer(marker);
				}else if(codigo == "4") {
					capital.addLayer(marker);
				}else{
					naoident.addLayer(marker);
				}
			} catch (err) {
					naoident.addLayer(marker);
			}
					oms.addMarker(marker);
					markersArray.push(marker);
					appendTableEntry('mapped', entry, mappedRowClass);
				});
			} else {
				appendTableEntry('notmapped', entry, notMappedRowClass);
			}
		});
	}

	map.addLayer(corrente);
	map.addLayer(capital);
	map.addLayer(naoident);
var controle = L.control.layers();
controle.addOverlay(corrente, "Corrente");
controle.addOverlay(capital, "Capital");
controle.addOverlay(naoident, "Não identificado");
controle.addTo(map);


	function drawCharts(metadata) {
		
		var tipo1 = metadata.tipo_1;
		var tipo2 = metadata.tipo_2;
		var tipo3 = metadata.tipo_3;
		var tipo4 = metadata.tipo_4;
		
	 Highcharts.setOptions({
				 lang: {
							 thousandsSep: '.',
							 decimalPoint: ','
									 }
					   });



	$(function () {
		$('#chart-quantity-wrapper').highcharts({
			chart: {
				plotBackgroundColor: null,
				plotBorderWidth: null,
				plotShadow: false
			},
			title: {
				text: 'Quantidade de cada tipo de despesa'
			},
			tooltip: {
				pointFormat: '<b>{point.y}</b>'
			},
			plotOptions: {
				pie: {
					allowPointSelect: true,
					cursor: 'pointer',
					dataLabels: {
						enabled: true,
				distance: -70,
						format: '<b>{point.name}</b>: {point.percentage:.1f} %',
				style: {
							fontWeight: 'bold',
							color: 'white',
							textShadow: '0px 1px 2px black'
						}
					}
				}
			},
			series: [{
				type: 'pie',
				name: 'Despesas',
				data: [
					['Mapeado',   tipo3.quantidade + tipo4.quantidade],
					['Não Mapeado', tipo1.quantidade + tipo2.quantidade],
				]
			}]
		});
	});



	$(function () {
			$('#chart-values-wrapper').highcharts({
				chart: {
					type: 'column'
				},
				title: {
					text: 'Distribuição de recursos por tipo de despesa'
				},
				xAxis: {
					categories: ['Orçado', 'Atualizado', 'Empenhado', 'Liquidado']
				},
				yAxis: {
					min: 0,
					title: {
						text: 'Despesas em bilhões de reais'
					},
			labels: {
				formatter: function () { return this.value/1000000000; }
			},
				},
				legend: {
					align: 'right',
					x: -70,
					verticalAlign: 'top',
					y: 20,
					floating: true,
					backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
					borderColor: '#CCC',
					borderWidth: 1,
					shadow: false
				},
				tooltip: {
				headerFormat: '{point.series.name}<br/>',
			pointFormat: '<b>R${point.y:,.2f}</b>'
					//formatter: function() {
					//    return '<b>'+ this.x +'</b><br/>'+
					//        this.series.name +': R$'+ this.y +'<br/>'+
					//        'Total: R$'+ this.point.stackTotal;
					//}
				},
				plotOptions: {
					column: {
						stacking: 'normal',
						dataLabels: {
							enabled: false,
							color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
							style: {
								textShadow: '0 0 3px black, 0 0 3px black'
							}
						}
					}
				},
				series: [{
					name: 'Mapeado',
					data: [tipo3.orcado + tipo4.orcado, tipo3.atualizado + tipo4.atualizado, tipo3.empenhado + tipo4.empenhado, tipo3.liquidado + tipo4.liquidado]
				}, {
					name: 'Não Mapeado',
					data: [tipo1.orcado + tipo2.orcado, tipo1.atualizado + tipo2.atualizado, tipo1.empenhado + tipo2.empenhado, tipo1.liquidado + tipo2.liquidado]
				}]
			});
		});

	}

	// Code starts here
	$.getJSON(path + 'geocoded.json', function(data) {
		drawMarkers(data.data);
	});

	window.prepararGrafTabs = function() {
		$.getJSON(path + 'geocoded.json', function(data) {
			$('#mapped-list-wrapper').html(mapped_list_html + '</table>');
			$('#notmapped-list-wrapper').html(notmapped_list_html + '</table>');
			drawCharts(data.metadata);
		});
	}
	
	window.markersArray = markersArray;
	window.map = map;
}

function gotoMarker(i) {
	map.setView(markersArray[i]._latlng, 16);
	$('html, body').animate({ scrollTop: $('#map').offset().top }, 'slow' );
	window.abrirPopup(markersArray[i]);
}

function carregarGrafTabs() {
	window.prepararGrafTabs();
	$("#graficos-tabelas").css("display", "block");
	$("#botao-graf-tab").css("display", "none");
}

function codeAddress() {
  var address = document.getElementById('address').value;
  var link = 'http://nominatim.openstreetmap.org/search/' + address + '?format=json&limit=1&countrycodes=br&viewbox=-47.16,-23.36,-45.97,-23.98&bounded=1';
  $.getJSON( link, function( data ) {
	if (data) {
		map.setView([data[0].lat,data[0].lon], 16);
	} else {
	      alert('Geocode was not successful');
	}
  });
}
