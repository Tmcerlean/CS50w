// Amadeus origin airport search
$(document).ready(function () {
    $("#inputOrigin").autocomplete({
        source: "{% url 'origin_airport_search'%}",
        minLength: 1,
        delay: 200,
    });
});