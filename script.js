async function getCommits() {
    let user = "insper-classroom"
    let repo = "projeto-pygame-oliva"

    let url = `https://api.github.com/repos/${user}/${repo}/commits?per_page=100`

    let response = await fetch(url, {method : "GET", headers : {}})
    let responseData = await response.json()

    let container = document.querySelector("#commits")
    for (let i in responseData) {
        container.innerHTML += `<p>${responseData[i].commit.author.name} - ${responseData[i].commit.message} | ${responseData[i].commit.author.date}</p>`
    }
}

getCommits()