const RSA = require("./index.js");

const public_n = 7688866313942546847852841551516404871721245684773845195430852158930371871231218035664083003138628808201116911937599329624356014626181704331364553496872303;
const public_e = 65537;

const message = "Hello, world !";
const encrypted_message = RSA.encrypt(RSA.encode(message), public_n , public_e);
console.log(encrypted_message.toString());
