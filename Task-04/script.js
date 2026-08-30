const cryptoBox = document.getElementById("cryptoBox")
const refreshButton = document.getElementById("refreshButton")
const searchInput = document.getElementById("searchInput")
const searchButton = document.getElementById("searchButton")
const priceChart = document.getElementById("priceChart")

let chart
let coins = []

async function getData() {
  cryptoBox.innerHTML = "<p>Loading...</p>"

  try {
    const response = await fetch(
      "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=25&page=1&sparkline=false"
    )

    coins = await response.json()

    displayData(coins)
  } catch (error) {
    cryptoBox.innerHTML = "<p>Could not load cryptocurrency data.</p>"

    console.error(error)
  }
}

function createChart(prices) {
  if (chart) {
    chart.destroy()
  }

  const labels = prices.map(price => new Date(price[0]).toLocaleDateString())

  const values = prices.map(price => price[1])

  chart = new Chart(priceChart, {
    type: "line",

    data: {
      labels: labels,

      datasets: [{
        label: "Price",
        data: values,
        borderWidth: 2
      }]
    },

    options: {
      responsive: true
    }
  })
}

async function getChartData(coinID) {
  const response = await fetch(
    `https://api.coingecko.com/api/v3/coins/${coinID}/market_chart?vs_currency=usd&days=7`
  )

  const data = await response.json()

  createChart(data.prices)
}

function displayData(coins) {
  cryptoBox.innerHTML = ""

  coins.forEach(function (coin) {
    const card = document.createElement("div")

    card.classList.add("crypto-card")

    const changeClass = coin.price_change_percentage_24h >= 0 ? "positive" : "negative"

    card.innerHTML = `
      <h2>${coin.name}</h2>

      <p>${coin.symbol.toUpperCase()}</p>

      <p class="price">
        $${coin.current_price.toLocaleString()}
      </p>

      <p class="${changeClass}">
        24h: ${coin.price_change_percentage_24h.toFixed(2)}%
      </p>

      <p>
        Market Cap:
        $${coin.market_cap.toLocaleString()}
      </p>

      <p>
        Volume:
        $${coin.total_volume.toLocaleString()}
      </p>
    `

    cryptoBox.appendChild(card)
  })
}

function searchCrypto() {
  const search = searchInput.value.toLowerCase()

  const results = coins.filter(coin =>
    coin.name.toLowerCase().includes(search) || coin.symbol.toLowerCase().includes(search)
  )

  displayData(results)
  if (results.length > 0) {
    getChartData(results[0].id)
  }
}


refreshButton.addEventListener("click", getData)
searchButton.addEventListener("click", searchCrypto)
getChartData()