/* Menu mobile accessible au clavier et au tactile. */
const boutonMenu = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#navigation");

if (boutonMenu && navigation) {
  boutonMenu.addEventListener("click", () => {
    const ouvert = boutonMenu.getAttribute("aria-expanded") === "true";
    boutonMenu.setAttribute("aria-expanded", String(!ouvert));
    navigation.classList.toggle("is-open", !ouvert);
  });
}
