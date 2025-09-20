class HiringHelper {
  constructor() {
    this.filteredCandidates = null
    this.rankedResults = null
    this.init()
  }

  init() {
    this.bindEvents()
    this.loadCandidateTicker()
    this.checkServerStatus()
  }

  bindEvents() {
    // Filter & Rank button
    document.getElementById("filter-rank-btn").addEventListener("click", () => {
      this.filterAndRank()
    })

    // Add candidate form
    document.getElementById("add-candidate-form").addEventListener("submit", (e) => {
      e.preventDefault()
      this.addCandidate()
    })

    // Export button
    document.getElementById("export-btn").addEventListener("click", () => {
      this.exportResults()
    })

    // Enter key on position input
    document.getElementById("position-input").addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        this.filterAndRank()
      }
    })
  }

  async checkServerStatus() {
    try {
      const response = await fetch("/health")
      const data = await response.json()

      const statusEl = document.getElementById("status")
      if (data.gemini_api_key_set) {
        statusEl.textContent = `Ready! ${data.candidates_loaded} candidates loaded.`
        statusEl.className = "status success"
      } else {
        statusEl.textContent = "Warning: GEMINI_API_KEY not set. Set environment variable and restart server."
        statusEl.className = "status error"
      }
    } catch (error) {
      const statusEl = document.getElementById("status")
      statusEl.textContent = "Error: Cannot connect to server."
      statusEl.className = "status error"
    }
  }

  async loadCandidateTicker() {
    try {
      const response = await fetch("/candidates")
      const candidates = await response.json()
      this.updateTicker(candidates)
    } catch (error) {
      console.error("Error loading candidates:", error)
    }
  }

  updateTicker(candidates) {
    const tickerContent = document.getElementById("ticker-content")
    tickerContent.innerHTML = ""

    candidates.forEach((name) => {
      const item = document.createElement("div")
      item.className = "ticker-item"
      item.textContent = name
      tickerContent.appendChild(item)
    })

    // Duplicate items for seamless scrolling
    candidates.forEach((name) => {
      const item = document.createElement("div")
      item.className = "ticker-item"
      item.textContent = name
      tickerContent.appendChild(item)
    })
  }

  async addCandidate() {
    const name = document.getElementById("candidate-name").value.trim()
    const email = document.getElementById("candidate-email").value.trim()
    const skills = document.getElementById("candidate-skills").value.trim()
    const salary = document.getElementById("candidate-salary").value

    if (!name) {
      alert("Name is required")
      return
    }

    try {
      const response = await fetch("/add_candidate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          email,
          skills,
          salary: salary ? Number.parseInt(salary) : 0,
        }),
      })

      if (response.ok) {
        // Clear form
        document.getElementById("add-candidate-form").reset()

        // Reload ticker
        this.loadCandidateTicker()

        // Show success message
        this.showMessage("Candidate added successfully!", "success")
      } else {
        const error = await response.json()
        this.showMessage(error.error || "Error adding candidate", "error")
      }
    } catch (error) {
      this.showMessage("Network error adding candidate", "error")
    }
  }

  async filterAndRank() {
    const position = document.getElementById("position-input").value.trim()

    if (!position) {
      alert("Please enter a job position")
      return
    }

    this.showLoading()
    this.hideResults()
    this.hideError()

    try {
      // Step 1: Filter candidates
      const filterResponse = await fetch("/filter", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ position }),
      })

      if (!filterResponse.ok) {
        throw new Error("Failed to filter candidates")
      }

      const filterData = await filterResponse.json()
      this.filteredCandidates = filterData

      if (filterData.candidates.length === 0) {
        this.showError("No candidates found matching the position requirements.")
        return
      }

      // Step 2: Rank candidates with Gemini
      const rankResponse = await fetch("/rank", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          job_title: position,
          candidates: filterData.candidates,
        }),
      })

      if (!rankResponse.ok) {
        const errorData = await rankResponse.json()
        throw new Error(errorData.error || "Failed to rank candidates")
      }

      this.rankedResults = await rankResponse.json()
      this.displayResults()
    } catch (error) {
      console.error("Error:", error)
      this.showError(error.message || "An error occurred while processing candidates.")
    } finally {
      this.hideLoading()
    }
  }

  displayResults() {
    const resultsSection = document.getElementById("results-section")
    const resultsList = document.getElementById("results-list")

    resultsList.innerHTML = ""

    if (!this.rankedResults || !this.rankedResults.ranked_candidates) {
      this.showError("Invalid ranking results received")
      return
    }

    // Create summary
    const summary = document.createElement("div")
    summary.className = "results-summary"
    summary.innerHTML = `
            <p><strong>Position:</strong> ${this.rankedResults.job_title}</p>
            <p><strong>Candidates Ranked:</strong> ${this.rankedResults.ranked_candidates.length}</p>
            ${this.rankedResults.selection_reasoning ? `<p><strong>Selection Reasoning:</strong> ${this.rankedResults.selection_reasoning}</p>` : ""}
        `
    resultsList.appendChild(summary)

    // Create candidate cards
    this.rankedResults.ranked_candidates.forEach((candidate) => {
      const card = this.createCandidateCard(candidate)
      resultsList.appendChild(card)
    })

    resultsSection.classList.remove("hidden")
    document.getElementById("export-btn").disabled = false
  }

  createCandidateCard(candidate) {
    const card = document.createElement("div")
    card.className = "candidate-card"

    const header = document.createElement("div")
    header.className = "candidate-header"
    header.innerHTML = `
            <div class="candidate-info">
                <h4>${candidate.name}</h4>
                <div class="candidate-meta">
                    ${candidate.email ? `Email: ${candidate.email}` : "No email provided"}
                </div>
            </div>
            <div class="candidate-scores">
                <span class="rank-badge">Rank #${candidate.rank}</span>
                <span class="score-badge">${candidate.final_score || candidate.match_score}%</span>
            </div>
        `

    const details = document.createElement("div")
    details.className = "candidate-details"

    let detailsHTML = ""

    if (candidate.strengths && candidate.strengths.length > 0) {
      detailsHTML += `
                <div class="strengths">
                    <h5>Strengths</h5>
                    <ul>
                        ${candidate.strengths.map((strength) => `<li>${strength}</li>`).join("")}
                    </ul>
                </div>
            `
    }

    if (candidate.weaknesses && candidate.weaknesses.length > 0) {
      detailsHTML += `
                <div class="weaknesses">
                    <h5>Areas for Consideration</h5>
                    <ul>
                        ${candidate.weaknesses.map((weakness) => `<li>${weakness}</li>`).join("")}
                    </ul>
                </div>
            `
    }

    if (candidate.why_on_top) {
      detailsHTML += `
                <div class="reasoning">
                    <strong>Why ranked highly:</strong> ${candidate.why_on_top}
                </div>
            `
    }

    if (candidate.why_on_bottom) {
      detailsHTML += `
                <div class="reasoning">
                    <strong>Ranking rationale:</strong> ${candidate.why_on_bottom}
                </div>
            `
    }

    details.innerHTML = detailsHTML

    // Toggle details on header click
    header.addEventListener("click", () => {
      details.classList.toggle("expanded")
    })

    card.appendChild(header)
    card.appendChild(details)

    return card
  }

  exportResults() {
    if (!this.rankedResults) {
      alert("No results to export")
      return
    }

    const dataStr = JSON.stringify(this.rankedResults, null, 2)
    const dataBlob = new Blob([dataStr], { type: "application/json" })

    const link = document.createElement("a")
    link.href = URL.createObjectURL(dataBlob)
    link.download = `ranked_candidates_${new Date().toISOString().split("T")[0]}.json`
    link.click()
  }

  showLoading() {
    document.getElementById("loading").classList.remove("hidden")
    document.getElementById("filter-rank-btn").disabled = true
  }

  hideLoading() {
    document.getElementById("loading").classList.add("hidden")
    document.getElementById("filter-rank-btn").disabled = false
  }

  showResults() {
    document.getElementById("results-section").classList.remove("hidden")
  }

  hideResults() {
    document.getElementById("results-section").classList.add("hidden")
  }

  showError(message) {
    document.getElementById("error-message").textContent = message
    document.getElementById("error-section").classList.remove("hidden")
  }

  hideError() {
    document.getElementById("error-section").classList.add("hidden")
  }

  showMessage(message, type) {
    // Simple toast-like message (you could enhance this)
    const toast = document.createElement("div")
    toast.className = `toast ${type}`
    toast.textContent = message
    toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 4px;
            color: white;
            background-color: ${type === "success" ? "#27ae60" : "#e74c3c"};
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `

    document.body.appendChild(toast)

    setTimeout(() => {
      toast.remove()
    }, 3000)
  }
}

// Initialize the app when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new HiringHelper()
})
