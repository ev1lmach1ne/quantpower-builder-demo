import {Config} from '@remotion/cli/config';

// En este entorno se usa el Chromium sin interfaz ya instalado.
if (process.env.REMOTION_CHROME) {
  Config.setBrowserExecutable(process.env.REMOTION_CHROME);
}
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
