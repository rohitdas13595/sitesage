import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import URLForm from "./URLForm";
import { fetchWithAuth } from "@/lib/api";

// Mock the api module
jest.mock("@/lib/api", () => ({
  API_ENDPOINTS: {
    ANALYZE: "/api/v1/seo/analyze",
  },
  fetchWithAuth: jest.fn(),
}));

describe("URLForm Component", () => {
  const mockOnAnalysisComplete = jest.fn();
  const placeholderRegex =
    /https:\/\/example\.com[\s\S]*https:\/\/another\.com/;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders correctly", () => {
    render(<URLForm onAnalysisComplete={mockOnAnalysisComplete} />);
    expect(screen.getByPlaceholderText(placeholderRegex)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /Analyze URL/i })
    ).toBeInTheDocument();
  });

  it("updates input value when typing", () => {
    render(<URLForm onAnalysisComplete={mockOnAnalysisComplete} />);
    const input = screen.getByPlaceholderText(placeholderRegex);
    fireEvent.change(input, { target: { value: "https://google.com" } });
    expect(input).toHaveValue("https://google.com");
  });

  it("submits the form and handles success", async () => {
    (fetchWithAuth as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    });

    render(<URLForm onAnalysisComplete={mockOnAnalysisComplete} />);
    const input = screen.getByPlaceholderText(placeholderRegex);
    const button = screen.getByRole("button", { name: /Analyze URL/i });

    fireEvent.change(input, { target: { value: "https://google.com" } });
    fireEvent.click(button);

    expect(screen.getByText(/Analyzing.../i)).toBeInTheDocument();

    await waitFor(() => {
      expect(fetchWithAuth).toHaveBeenCalledWith(
        "/api/v1/seo/analyze",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ url: "https://google.com" }),
        })
      );
    });

    await waitFor(() => {
      expect(
        screen.getByText(/Analysis completed successfully!/i)
      ).toBeInTheDocument();
    });

    expect(mockOnAnalysisComplete).toHaveBeenCalled();
  });

  it("submits batch analysis for multiple URLs", async () => {
    (fetchWithAuth as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => [{}, {}],
    });

    render(<URLForm onAnalysisComplete={mockOnAnalysisComplete} />);
    const input = screen.getByPlaceholderText(placeholderRegex);
    const button = screen.getByRole("button", { name: /Analyze URL/i });

    fireEvent.change(input, {
      target: { value: "https://google.com\nhttps://bing.com" },
    });
    fireEvent.click(button);

    await waitFor(() => {
      expect(fetchWithAuth).toHaveBeenCalledWith(
        "/api/v1/seo/analyze/batch",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            urls: ["https://google.com", "https://bing.com"],
          }),
        })
      );
    });

    expect(mockOnAnalysisComplete).toHaveBeenCalled();
  });

  it("handles API error", async () => {
    (fetchWithAuth as jest.Mock).mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: "Invalid URL" }),
    });

    render(<URLForm onAnalysisComplete={mockOnAnalysisComplete} />);
    const input = screen.getByPlaceholderText(placeholderRegex);
    const button = screen.getByRole("button", { name: /Analyze URL/i });

    fireEvent.change(input, { target: { value: "https://error.com" } });
    fireEvent.click(button);

    const errorMessage = await screen.findByText("Invalid URL");
    expect(errorMessage).toBeInTheDocument();

    expect(mockOnAnalysisComplete).not.toHaveBeenCalled();
  });
});
