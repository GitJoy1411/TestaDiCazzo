// Genera un numero segreto casuale tra 1 e 100
let numeroSegreto = Math.floor(Math.random() * 100) + 1;

// Funzione per controllare l'indovinello
function controllaIndovinello() {
    let indovinato = parseInt(document.getElementById("guess").value);

    if (indovinato === numeroSegreto) {
        document.getElementById("risultato").innerHTML = "Hai indovinato! Il numero era " + numeroSegreto;
    } else if (indovinato > numeroSegreto) {
        document.getElementById("risultato").innerHTML = "Troppo alto! Prova un numero più piccolo.";
    } else {
        document.getElementById("risultato").innerHTML = "Troppo basso! Prova un numero più grande.";
    }
}
