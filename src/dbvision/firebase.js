import { initializeApp } from 'firebase/app';
import {
  GoogleAuthProvider,
  getAuth,
  onAuthStateChanged,
  signInWithPopup,
  signOut,
} from 'firebase/auth';

// Configuração WEB do projeto Firebase "amauryesp-active": estes valores são públicos, feitos para ficar no site.
// NÃO colocar aqui senha de banco nem chave secreta: tudo que fica no site é público.
const app = initializeApp({
  apiKey: 'AIzaSyDBODTirHnnNE6BCwIU2kAt0lV6uo5_ReY',
  authDomain: 'amauryesp-active.firebaseapp.com',
  projectId: 'amauryesp-active',
  appId: '1:583072177641:web:ac07d0af4aa1e208013f78',
});

// Login Google: usado só no UPLOAD. A API confere o e-mail permitido (EMAIL_PERMITIDO no Render).
export const auth = getAuth(app);
export const entrar = () => signInWithPopup(auth, new GoogleAuthProvider());
export const sair = () => signOut(auth);
export const aoMudarLogin = (fn) => onAuthStateChanged(auth, fn);
