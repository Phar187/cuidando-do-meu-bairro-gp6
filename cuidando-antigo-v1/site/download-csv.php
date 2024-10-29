<?php
	$year = $_GET['year'];
	$orgao = $_GET['orgao'];
	
	header('Content-type: text/csv');
	header('Content-Disposition: attachment; filename="' . $orgao . '.csv"');
	
	$path = "data/" . $year . "/orgaos.json";
	$json = file_get_contents($path);
	$data = json_decode($json, TRUE);
	$content = $data[$orgao];
	
	$csv = "Orgao;Unidade;Funcao;Subfuncao;Programa;Projeto/Atividade;Orcado;Atualizado;Empenhado;Liquidado;Mapeado";
	$csv .= "\n" . implode("\n", $content);
	echo $csv;
?>
