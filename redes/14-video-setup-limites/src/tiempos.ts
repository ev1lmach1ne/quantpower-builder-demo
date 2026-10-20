import tiempos from './tiempos.json';

export const FPS = 30;
// Margen tras cada frase para que la escena respire
const PAUSA = 0.6;

export type Escena = {
  id: string;
  titulo: string;
  texto: string;
  audio: string;
  inicio: number; // fotograma
  duracion: number; // fotogramas
};

let cursor = 0;
export const ESCENAS: Escena[] = tiempos.map((t) => {
  const duracion = Math.ceil((t.dur + PAUSA) * FPS);
  const e = {...t, inicio: cursor, duracion};
  cursor += duracion;
  return e;
});
// La escena final se alarga para dejar la llamada a la acción en pantalla
ESCENAS[ESCENAS.length - 1].duracion += 2 * FPS;
export const DURACION_TOTAL = ESCENAS.reduce((s, e) => s + e.duracion, 0);

export const escena = (id: string) => ESCENAS.find((e) => e.id === id)!;
