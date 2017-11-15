function afficher_evenement (evenement)
	{
		zoom = jQuery('#zoom')
		zoom.empty()
		zoom.append("<li>"evenement.titre"</li>")
		zoom.append("<li>"evenement.lieu"</li>")	
		zoom.append("<li>"evenement.date"</li>")
			
	}