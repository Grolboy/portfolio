<?php include 'need.php'; ?>

<div class="typed-container">
  <h1 style="font-weight: 600; font-size: 2.5rem; color: var(--primary-color); margin-bottom: 0.5rem;">
    👋 Hi, I'm <b>Lucas Ingmar</b>.
  </h1>
  <h2 style="font-weight: 400; font-size: 1.8rem; color: var(--secondary-color); white-space: nowrap; min-height: 2.2rem; display: flex; align-items: center;">
    <span id="emoji" style="margin-right: 0.5rem; font-size: 1.8rem;">🔧</span>
    <span>I enjoy </span>
    <span id="rotating-text" style="border-right: 3px solid var(--secondary-color); padding-left: 0.3rem; white-space: nowrap;"></span>
  </h2>
</div>

<script>
  document.addEventListener('DOMContentLoaded', function () {
    const lines = [
      { emoji: "💪🏽", text: "working with computers and my hands." },
      { emoji: "🔍", text: "exploring code, security and other things ICT." },
      { emoji: "🧰", text: "repairing things." },
      { emoji: "🛠️", text: "modifying things." }
    ];

    function randomSpeed(min = 50, max = 120) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function typeText(element, text) {
      return new Promise((resolve) => {
        let index = 0;
        element.innerHTML = '';

        function typeChar() {
          if (index < text.length) {
            element.innerHTML += text[index];
            index++;
            setTimeout(typeChar, randomSpeed(40, 100));
          } else {
            setTimeout(resolve, 1500);
          }
        }
        typeChar();
      });
    }

    function eraseText(element) {
      return new Promise((resolve) => {
        let length = element.innerHTML.length;

        function eraseChar() {
          if (length > 0) {
            element.innerHTML = element.innerHTML.slice(0, length - 1);
            length--;
            setTimeout(eraseChar, 40);
          } else {
            setTimeout(resolve, 500);
          }
        }
        eraseChar();
      });
    }

    async function rotate() {
      const emojiEl = document.getElementById('emoji');
      const textEl = document.getElementById('rotating-text');

      while (true) {
        for (const line of lines) {
          emojiEl.textContent = line.emoji;
          await typeText(textEl, line.text);
          await eraseText(textEl);
        }
      }
    }

    rotate();
  });
</script>
