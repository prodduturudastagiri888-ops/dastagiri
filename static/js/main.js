// Smart Krishi - Core Client Interactions

document.addEventListener("DOMContentLoaded", () => {
  // 1. Low Bandwidth Mode Toggle
  const lowBwBtn = document.getElementById("toggleLowBandwidthBtn");
  const isLowBw = localStorage.getItem("smart_krishi_low_bw") === "true";
  
  if (isLowBw) {
    document.body.classList.add("low-bandwidth-mode");
    if (lowBwBtn) lowBwBtn.classList.add("active");
  }

  if (lowBwBtn) {
    lowBwBtn.addEventListener("click", () => {
      const active = document.body.classList.toggle("low-bandwidth-mode");
      localStorage.setItem("smart_krishi_low_bw", active);
      lowBwBtn.classList.toggle("active", active);
    });
  }

  // 2. Leaf Photo Drag & Drop Preview Handler
  const dropzone = document.getElementById("leafDropzone");
  const fileInput = document.getElementById("leafFileInput");
  const previewImg = document.getElementById("leafPreviewImg");
  const previewBox = document.getElementById("leafPreviewContainer");

  if (dropzone && fileInput) {
    dropzone.addEventListener("click", () => fileInput.click());

    dropzone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    });

    dropzone.addEventListener("dragleave", () => {
      dropzone.classList.remove("dragover");
    });

    dropzone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        fileInput.files = e.dataTransfer.files;
        showPreview(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener("change", () => {
      if (fileInput.files && fileInput.files[0]) {
        showPreview(fileInput.files[0]);
      }
    });

    function showPreview(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        if (previewImg && previewBox) {
          previewImg.src = e.target.result;
          previewBox.style.display = "block";
        }
      };
      reader.readAsDataURL(file);
    }
  }

  // 3. Offline Farming Advice Cache (Feature 6)
  if ("localStorage" in window) {
    // If on a page with advice, cache it
    const adviceEl = document.querySelector(".cacheable-advice");
    if (adviceEl) {
      const pageKey = window.location.pathname;
      localStorage.setItem(`advice_cache_${pageKey}`, adviceEl.innerHTML);
    }

    // Network status listener
    window.addEventListener("offline", () => {
      showConnectivityBanner(false);
    });
    window.addEventListener("online", () => {
      showConnectivityBanner(true);
    });

    if (!navigator.onLine) {
      showConnectivityBanner(false);
    }
  }

  function showConnectivityBanner(online) {
    let banner = document.getElementById("offlineStatusBanner");
    if (!banner) {
      banner = document.createElement("div");
      banner.id = "offlineStatusBanner";
      banner.className = "alert alert-warning py-2 mb-0 text-center sticky-top";
      document.body.prepend(banner);
    }

    if (!online) {
      banner.style.display = "block";
      banner.innerHTML = `<strong>⚠️ Offline Mode:</strong> Showing previously saved farming advice from local memory. Connect to internet for live weather and market data.`;
    } else {
      banner.style.display = "none";
    }
  }
});
