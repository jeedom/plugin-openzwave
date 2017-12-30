/******************************************************************
***
*** Fonction customJS permet des modification du thème pour la 
*** doc github
***
*** Paramètre optionelle(s)
*** - numTitre : true (defaut) peux prendre false, permet d'ajouter 
***    les numéro de chapitre au titre des chapitre et sous titre
*** - menuType : 1 (defaut) permet de choisir pour le type de menu
***    pour le moment il ni as qu'une seule version
*** - linkSommaire : permet de choisir le type de lien en version 
***     mobile pour le retrous en haut de page
********************************************************************/
(function($) {
        $.fn.customJS = function(settings) {
                /*** Configuration par défaut ***/
                var config = {
                    menuType: 1,
                    numTitre: true,
                    linkSommaire : 'link'
                };
                
                /*** Chargement de paramètre user ***/
                if (settings) {
                    $.extend(config, settings);
                }
                
                var contTitres = $(this);
                
                /*** Ajout des numéros de chapitre au titre des chapitres et leut sous titres ***/
                if(config.numTitre){
                        var i = 1, j = 1;
                        $('h1, h2', contTitres).each(function(){
                                if($(this)[0].tagName.toLowerCase() == 'h1'){
                                        $('#'+$(this).attr('id')).text(i + '. ' + $(this).text());
                                        i++;
                                } 
                                if($(this)[0].tagName.toLowerCase() == 'h2'){
                                        $('#'+$(this).attr('id')).text( (i-1) + '.' + j + ' ' + $(this).text()); 
                                        j++;
                                }else{
                                        j = 1;
                                }
                        });  
                }
                
                /*** Rend clicable le titre du sommaire pour un retour de scroll à 0 ***/
                $('#toctitle h2').wrap( '<a href="#main_content"></a>').on('clic', function(){
                        $('#main_content').scrollTop(0);
                });
                 
                /*** effet sur scroll du header ***/
                if($('.toctoggle:visible').length == 0){
                        var header = $('.page-header')[0];
                        var contenu = $('#main_content')[0];
                        var menu = $('#menu-sommaire')[0];
                        
                        /* Fonction scrollY pour une compatibilité avec tout les nav*/
                        var scrollY = function(){
                                var supportPageOffset = window.pageXOffset !== undefined;
                                var isCSS1Compat = ((document.compatMode || "") === "CSS1Compat");
                                return supportPageOffset ? window.pageYOffset : isCSS1Compat ? document.documentElement.scrollTop : document.body.scrollTop;       
                        }
                        var top = header.getBoundingClientRect().top + scrollY() + 100;
                        $('#menu-sommaire').height( $(window).height() - $('.page-header').height() );
                        
                        
                        /*Fonction executé au scroll*/
                        var onScroll = function(){
                                var isClassScroll = header.classList.contains('header-min');
                                if(scrollY() > top && !isClassScroll){
                                        header.classList.add('header-min');
                                        $('#logo_jeedom',header).removeClass('animLogoJeedomHaut');
                                        contenu.classList.add('contenu-main-min');
                                        menu.classList.add('menu-header-min');
                                        $('#menu-sommaire').height( $(window).height() - $('.page-header').height() );
                                }else if(scrollY() < top && isClassScroll){
                                        header.classList.remove('header-min');
                                        $('#logo_jeedom',header).addClass('animLogoJeedomHaut');
                                        contenu.classList.remove('contenu-main-min');
                                        menu.classList.remove('menu-header-min');
                                        $('#menu-sommaire').height( $(window).height()-$('.page-header').height() );
                                }
                        }
                        window.addEventListener('scroll', onScroll);
                }
                
                /*** Ajout des liens retour au sommaire ***/
                if(config.linkSommaire == 'link'){
                    $('#main_content h1:gt(0), #main_content h2').before('<p><a class="linkToTop" href="#toctitle" title="'+ config.traduction.key_do_not_edit_titreMenu +'">'+ config.traduction.key_do_not_edit_titreMenu +'</a></p>');
                }
				
				/*** Renomme les boutons langues ***/
				$('#blocLangs a.btn').each(function(){
					$(this).text($(this).data('lang').substr(0, 2));	
				});
				
				/*** Fonction de scrolling ***/
				var a = sessionStorage.getItem('anchor'), yPos, yInitPos, target;
 
				function scrolling(href, p){

				  yInitPos = $(window).scrollTop();

				  // On ajoute le hash dans l'url.
				  window.location.hash = href;

				  // Comme il est possible que l'ajout du hash perturbe le défilement, on va forcer le scrollTop à son endroit inital.
				  if(a) $(window).scrollTop(yInitPos);
				  else $(window).scrollTop(p);

				  
				  // On cible manuellement l'ancre pour en extraire sa position.
				  // Si c'est un ID on l'obtient.
				  target = ($(href + ":first"));
							
				  // Sinon on cherche l'ancre dans le name d'un a.
				  if (target.length == 0) {
					 target = ($("a[name=" + href.replace(/#/gi,"") + "]:first"))
				  }
								
				  // Si on a trouvé un name ou un id, on défile.
				  if (target.length == 1) {
					 yPos = target.offset().top; // Position de l'ancre.
								
					 // On anime le défilement jusqu'à l'ancre.
					 $('html,body').animate({ scrollTop: yPos - 85 }, 1000); // On décale de 85 pixels l'affichage pour ne pas coller le bord haut de l'affichage du navigateur et on défile en 1 seconde jusqu'à l'ancre.
				  }
				}

				if(a){ var href = a; scrolling(a); sessionStorage.removeItem('anchor'); }
				// Pour tous les liens commençant par #.
				$('#toc a').click(function (e) {

				  var href = $(this).attr('href'), t = new RegExp('#.*'), anchor = new RegExp('^#.*'), p = $(this).offset().top;
				  if(href.match(anchor)){ e.preventDefault(); scrolling(href, p); }else if(href.match(t)){
					 e.preventDefault();
					 sessionStorage.setItem('anchor', href.match(t));
					 location.href = href.replace(/#.*/, '');
				  }
				});
        
				//Ajout de la class active sur les liens menu des éléments affiché
				var idChapitre = null, nbrChapitre = 0, idAncre = null;
				
				$('#main_content h1, #main_content h2').on('inview',function(event, isInView, visiblePartX, visiblePartY){
					nbrChapitre = $('#toc a.active').length;
					idAncre = $(this).attr('id');
					if(isInView){
						$('#toc a[href="#'+ idAncre +'"]').addClass('active');
						if(idChapitre != null){
							$('#toc a[href="#'+ idChapitre +'"]').removeClass('active');
							idChapitre = null;
						}
					}else if (nbrChapitre > 1){
						$('#toc a[href="#'+ idAncre +'"]').removeClass('active');
					}else{
						idChapitre = idAncre;
					}
				});
		
		};
        return this;
})(jQuery);
