<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8">
    <title>Cuidando do meu Bairro</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

		<!--favicon-->
		<link rel="shortcut icon" href="img/favicon.ico" type="image/x-icon"/>

    <!--CSS Styles-->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/bootstrap-responsive.min.css" rel="stylesheet">
    <link href="css/docs.css" rel="stylesheet">
    <style type="text/css">
    	#hero-unit-pic img {
    		opacity: 0.5;
				/*Transition*/
				-webkit-transition: all 0.5s ease;
				-moz-transition: all 0.5s ease;
				-o-transition: all 0.5s ease;
			}
			#hero-unit-pic img:hover {opacity: 1;}
    </style>
    <!--END OF CSS Styles-->
    
    <!--Javascript-->
    <script src="http://code.jquery.com/jquery-latest.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/application.js"></script>

  </head>

  <body>
    <?php include("header.inc.php"); ?>

    <div class="container">
      <div class="hero-unit">
      	<div class="row">
      		<div class="span7">
      			<h1>Mapeando dinheiro do orçamento público.</h1>
      			<p style="text-align:justify; margin-top:5px;">Buscamos oferecer ferramentas para que a sociedade possa conhecer melhor a temática do orçamento público, exercer o controle e fiscalização dos gastos realizados em equipamentos públicos da cidade e promover ações concretas no seu bairro. Por este motivo, o projeto foi batizado de <strong>Cuidando do meu Bairro</strong></span>.</p>
      		</div>
      		<div id="hero-unit-pic" style="float:right;">
      			<a href="map.php?year=2014"><img title="Ir para a visualização de 2014" class="img-rounded" src="img/hero-unit-pic.png" width="350" height="250"></img></a>
      		</div>
      	</div> <!--Row-->
      </div> <!--Hero-Unit-->
    </div> <!--Container-->

    <?php include("footer.inc.php"); ?>
  </body>
</html>
