async function generateKeys() {
    const response = await fetch("/generate_keys", { method: "POST" });
    const data = await response.json();
    alert(data.message);
}

async function encryptMessage() {
    const message = document.getElementById("message").value;
    const response = await fetch("/encrypt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: message })
    });

    const data = await response.json();
    document.getElementById("result").innerText = `Message chiffré : ${data.encrypted_data}`;
}

async function decryptMessage() {
    const encryptedData = document.getElementById("message").value;
    const response = await fetch("/decrypt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: encryptedData })
    });

    const data = await response.json();
    document.getElementById("result").innerText = data.decrypted_data ? 
        ` Message déchiffré : ${data.decrypted_data}` : 
        " Erreur de déchiffrement.";
}
