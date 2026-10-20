import {Composition} from 'remotion';
import {SetupLimites} from './SetupLimites';
import {DURACION_TOTAL, FPS} from './tiempos';

export const RemotionRoot = () => {
  return (
    <Composition
      id="SetupLimites"
      component={SetupLimites}
      durationInFrames={DURACION_TOTAL}
      fps={FPS}
      width={1080}
      height={1920}
    />
  );
};
