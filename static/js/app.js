function buildMetadata(artist) {

  // Use `d3.json` to fetch the metadata for an artist
  // Use d3 to select the table
  var metadataURL = `/artists/${artist}`;
  d3.json(metadataURL).then(function(data){
  console.log(data);
    var rows = d3.select("tbody")
        .selectAll("tr")
        .data(data);
      
    rows.exit().remove();

    var trEnter = rows.enter()
        .append("tr");

    trEnter.html(function(d) {
          return `<td>${d.pub_year}</td><td>${d.title}</td><td>${d.url}</td>`;
        });

    var td = rows.selectAll("td").data(function(d) { return d3.values(d); });

    td.exit().remove();

    td.enter().append("td");
    td.text(function(d) { return d; });
    })
  };

function buildCharts(artist) {

    var plotdataURL = `/reviews/${artist}`;
    d3.json(plotdataURL).then(function(data){
      console.log(data);
      var albums = data.album;
      var years = data.pub_year;
      var scores = data.score;
      var genres = data.genre;

      var trace1 = {
        x: albums,
        y: scores,
        type: 'bar',
        text: genres,
        marker: {
          color: 'rgb(142,124,195)'
        }
      };
      
      var bar_plot = [trace1];
      
      var bar_layout = {
        title: 'Artist Album Scores',
        showlegend: false,
        xaxis: {
          title: "Album",
          tickangle: 45,
          automargin: true
        },
        yaxis: {
          title: "Score",
          range: [0, 10],
          zeroline: false,
          gridwidth: 2,
          automargin: true
        },
        bargap: 0.5
      };
      
      Plotly.newPlot('bar', bar_plot, bar_layout);
  });
};

function buildChartsGenre(genre) {

  var plotdataURL = `/themes/${genre}`;
  d3.json(plotdataURL).then(function(data){
    console.log(data);
    var years = data.pub_year;
    var scores = data.score;
    
    var trace1 = {
      x: years,
      y: scores,
      type: 'scatter'
    };
    
    var line_plot = [trace1];
    
    var line_layout = {
      title: 'Average Genre Scores By Year',
      font:{
        family: 'Raleway, sans-serif'
      },
      xaxis: {
        title: "Year",
        automargin: true
      },
      yaxis: {
        title: "Score",
        range: [0, 10],
        automargin: true
      }
    };
    
    Plotly.newPlot('line', line_plot, line_layout);

});
};

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");
  var selector_2 = d3.select("#selGenre");

  // Use the list of artist names to populate the select options
  d3.json("/artist_names").then((artistNames) => {
    artistNames.forEach((artist) => {
      selector
        .append("option")
        .text(artist)
        .property("value", artist);
    });

    // Use the first artist from the list to build the initial plots
    const firstArtist = artistNames[0];
    buildCharts(firstArtist);
    buildMetadata(firstArtist);
  });

  // Use the list of genres to populate the select options
  d3.json("/genres").then((genreNames) => {
    genreNames.forEach((genre) => {
      selector_2
        .append("option")
        .text(genre)
        .property("value", genre);
    });
    // Use the first genre from the list to build the initial plots
    const firstGenre = genreNames[0];
    buildChartsGenre(firstGenre);
  });
}

function optionChanged(newArtist) {
  // Fetch new data each time a new artist is selected
  buildCharts(newArtist);
  buildMetadata(newArtist);
}

function optionChangedGenre(newGenre) {
  // Fetch new data each time a new genre is selected
  buildChartsGenre(newGenre);
}

// Initialize the dashboard
init();