// script gerant l'affichage du graphique                  
 


                  bleu_ciel = '#0099FF'
                  rouge = '#ec5148'
                  noir = '#000000'
                  bleu_fonce = '#000066'
                  blanc = '#FFFFFF'
                  jaune_pale = '#FFFFCC'
                  gris = '#eee'
                  teal = '#3DAA90'
                  orange = '#EC5117'

                   
                    

                  var graph = graph.split('///')
                  var noeuds = graph[0].split('//')
                  var edges = graph[1].split('//')



                  var s = new sigma('container');

                  //creation des noeuds
                  for(var i= 1; i < noeuds.length; i++)
                            {    
                                 noeud = noeuds[i] ;
                                 noeud = noeud.split("/");
                                 s.graph.addNode({
                                                  // Main attributes:
                                                  id: noeud[0],
                                                  label: noeud[1],
                                                  // Display attributes:
                                                  x: noeud[2],
                                                  y: noeud[3],
                                                  size: noeud[4],
                                                
                                                })

                            }


                  //creation des edges
                  for(var i= 1; i < edges.length; i++)
                            {    
                                 edge = edges[i] ;
                                 edge = edge.split("/");
                                 s.graph.addEdge({
                                                  id: edge[0],
                                                  // Reference extremities:
                                                  source: edge[1],
                                                  target: edge[2]

                                                })

                            }




                  //modification des paramètres du graph:
                   s.settings({
                              defaultNodeColor: orange,
                              DefaultNodeBorderColor: teal,
                              defaultLabelColor: noir,
                              defaultLabelSize : 15,
                              cloner : true,
                              labelThreshold : 1,
                              zoomingRatio : 1.0,
                              doubleClickZoomingRatio: 1.5,
                              ZoomMax: 1.0,
                              ZoomMin: 1.0,
                              SideMargin: 50,
                              scalingMode: "inside",
                              
                              });         

                  s.refresh(); 



                  //creation des fonctions du graph:

                        // We first need to save the original colors of our
                        // nodes and edges, like this:
                        s.graph.nodes().forEach(function(n) {
                          n.originalColor = n.color;
                        });
                        s.graph.edges().forEach(function(e) {
                          e.originalColor = e.color;
                        });

                        s.bind('clickNode', function(e) {

                          
                          var label = e.data.node.id
                          document.location.href="page_revendications.html?ennonce=" + label

                          var nodeId = e.data.node.id,
                              toKeep = s.graph.neighbors(nodeId);
                          toKeep[nodeId] = e.data.node;

                          s.graph.nodes().forEach(function(n) {
                            if (toKeep[n.id])
                              n.color = n.originalColor;
                            else
                              n.color = '#eee';
                          });

                          s.graph.edges().forEach(function(e) {
                            if (toKeep[e.source] && toKeep[e.target])
                              e.color = e.originalColor;
                            else
                              e.color = '#eee';
                          });

                          // Since the data has been modified, we need to
                          // call the refresh method to make the colors
                          // update effective.
                        s.refresh();
                        });