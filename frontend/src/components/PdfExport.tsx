"use client";

interface PdfExportProps {
  destination: string;
}

export function PdfExport({ destination }: PdfExportProps) {
  const handlePrint = () => {
    // Give the browser a title that becomes the PDF filename.
    const prev = document.title;
    document.title = `Wanderlust — ${destination} Trip Plan`;
    window.print();
    document.title = prev;
  };

  return (
    <button className="btn btn-ghost pdf-btn" onClick={handlePrint} title="Download as PDF">
      <svg fill="none" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round"
        strokeLinejoin="round" viewBox="0 0 24 24" width={18} height={18}>
        <path d="M12 3v12M8 11l4 4 4-4" />
        <path d="M4 17v1a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-1" />
      </svg>
      Download PDF
    </button>
  );
}
