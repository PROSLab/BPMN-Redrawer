// Type Declaration file to provide TypeScript type information about
// bpmn-js, which is written in JavaScript
declare module 'bpmn-js/lib/Modeler' {
  export interface WriterOptions {
    format?: boolean;
    preamble?: boolean;
  }
  export type DoneCallback = (err: unknown, warn: unknown) => void;

  export default class Modeler {
    constructor(options: { container: string; keyboard: { bindTo: Document } });

    importXML(xml: string): Promise<void>;
    saveXML(
      options: WriterOptions,
      done?: DoneCallback
    ): Promise<{ xml: string }>;
    saveXML(done?: DoneCallback): Promise<{ xml: string }>;
    saveSVG(
      options: WriterOptions,
      done?: DoneCallback
    ): Promise<{ svg: string }>;
    saveSVG(done?: DoneCallback): Promise<{ svg: string }>;
    on(event: string, func: () => void): void;
    off(event: string, func?: () => void): void;
    detach(): void;
  }
}
