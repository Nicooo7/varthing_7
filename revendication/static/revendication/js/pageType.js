//fonctions utilisées dans page_type.html

//___________________________________________materialize____________________________________________

jQuery.noConflict();
jQuery(document).ready(function()
          { 
  

            jQuery('.tooltipped').tooltip({delay: 50});
            jQuery('.dropdown-button').dropdown({
                                        inDuration: 300,
                                        outDuration: 225,
                                        constrainWidth: false, // Does not change width of dropdown to that of the activator
                                        hover: false, // Activate on hover
                                        gutter: 3, // Spacing from edge
                                        belowOrigin: true, // Displays dropdown below the button
                                        alignment: 'right', // Displays dropdown with edge aligned to the left of button
                                        stopPropagation: false // Stops event propagation
                                          });
            
             
            jQuery('select').material_select();
            jQuery('.parallax').parallax();
            jQuery('.carousel').carousel(); 
    
          });
 
                  


//_____________________________________________icalendar_______________________________________

           
              var evenements = evenements.split("ggg");
              var liste_evenement = new Array();
              for(var i= 0; i < evenements.length; i++)
                  {    
                       evenement = evenements[i] ;
                       evenement = evenement.split("/");
                       var evenement =  {title: evenement[0], start: evenement[1]};
                       liste_evenement.push(evenement);
                  }

              jQuery('#calendar').fullCalendar
                        ({
                            eventSources: 
                                [{
                                    events: liste_evenement,
                                    color: 'black',     // an option!
                                    textColor: 'yellow' // an option!
                                              
                                }],

                            defaultView: "listMonth",
                            eventClick: function(calEvent, jsEvent, view) 
                                {

                                    alert('Event: ' + calEvent.title);

                                    // change the border color just for fun
                                    jQuery(this).css('border-color', 'red');
                                }

                        });  
                        
           
  //__________________________________________auto-completion________________________________________________
       
                                  
                var completion = completion.split("&#39;").join("\'");
                var reg=new RegExp("_", "g");
                var tableau=completion.split(reg);
                jQuery('#recherche').autocomplete({source: tableau });
                jQuery('#recherche').trigger('autoresize');

                var lien = document.getElementById('lien');
                var recherche = document.getElementById('recherche');
                lien.onclick = function() 
                    {
                        document.location.href = "page_revendications.html?ennonce=" + recherche.value
                    }; 

                        
                         