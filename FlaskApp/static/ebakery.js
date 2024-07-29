$(document).ready(function() {
    
    function loadDefaultContent() {
        const contentDiv = $('.content');
        const defaultContent = '<h1>Willkommen auf meiner Webseite</h1><p>Bitte wählen Sie ein Projekt aus der Seitenleiste aus.</p>';
        contentDiv.html(defaultContent);
    }

    function updateContent(project) {
        const contentDiv = $('.content');
        console.log('updateContent aufgerufen mit Projekt:', project);
        // AJAX-Anfrage an den Server, um den Inhalt für das ausgewählte Projekt zu laden
        $.ajax({
            url: '/get_project',
            data: { project: project },
            type: 'GET',
            success: function(response) {
                contentDiv.html(response);
            },
            error: function() {
                contentDiv.html('<p>Fehler beim Laden des Inhalts.</p>');
            }
        });
    }

    const projectLinks = $('.sidebar ul a'); // Geändert
    projectLinks.click(function(event) {
        event.preventDefault();
        const project = $(this).text().trim();
        updateContent(project);
    });

    const defaultContentLink = $('.sidebar h3 a');
    defaultContentLink.click(function(event) {
        event.preventDefault();
        loadDefaultContent();
    });

    console.log('JavaScript-Datei geladen');
})