// Function to convert blob to Data URL string
// to use as image source
export function blobToDataURL(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader: FileReader = new FileReader();
    reader.onload = (ev: ProgressEvent<FileReader>) => {
      resolve(ev.target?.result as string);
    };
    reader.onerror = () => {
      reject();
    };
    reader.readAsDataURL(blob);
  });
}
