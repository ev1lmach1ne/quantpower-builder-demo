import {Composition} from 'remotion';
import {Eventos, DURACION, FPS} from './Eventos';

export const RemotionRoot = () => {
  return (
    <Composition id="Eventos" component={Eventos} durationInFrames={DURACION} fps={FPS} width={1080} height={1920} />
  );
};
