         
//DEFINITION DES FONCTIONS GLOBALES **************************************************
                  


                  //global:
                 carte_global = jQuery('[id*="carte"]')
                 filtre_global = jQuery('[id*="filtre"]')
                 bouton_global = jQuery('[id*="bouton"]')
                 badge_global = jQuery('[id*="badge"]')
                 Tableau_global = jQuery('[id*="Tableau"]')
                 Formulaire_global = jQuery('[id*="formulaire"]')

                 boutons = jQuery('[cible]')

                      
                  function masquer(){
                                filtre_global.hide()
                                jQuery("#graphique").hide()
                                Tableau_global.hide() 
                                Formulaire_global.hide()                           
                  }
                  

                  function bouton_actif(x){
                          
                          boutons.parent().css("border", "solid black 0px")
                          x.css("border", "solid black 2px") 
                                          }


                  function onglet(){
                             var onglet = "{{onglet}}"
                             if (onglet == "revendication"){
                                       jQuery("#bouton_revendications").click()
                                                        }
                             else if (onglet == "petition"){
                                        jQuery("#bouton_petitions").click()
                                                          }
                             else if (onglet == "evenement"){
                                      jQuery("#bouton_evenements").click()
                                                      }  
                             else if (onglet == "vide"){jQuery("#badge_liste").get(0).click();}
                                     }

                             

                  
                  boutons.click(function() {
                                bouton_actif(jQuery(this).parent())
                                var cible= "#"+ jQuery(this).attr('cible') 
                                masquer() 
                                jQuery(cible).show()                              
                                          });                   
  



// EVENEMENTS CROISES:

                  // REVENDICATIONS
               

                  // PETITIONS
                    


                  //EVENEMENTS
                    
                                          
                                         
                   //GRAPHIQUE

                    
                    jQuery('#badge_container').click(function() {
                                                  jQuery('#containers').empty()
                                                  var graph = "{{graph_accueil}}"; 
                                                  affichage_graphique(graph, "containers");
                                                  alert("devrait s'afficher")
                                                      });             
                    


                    //LISTE
                  


               
                  
                    masquer()
                    
                    

       
