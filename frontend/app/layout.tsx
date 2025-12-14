import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import ChatAssistant from "./components/ChatAssistant";
import { PredictionProvider } from "./context/PredictionContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AttritionAI - Prédiction Intelligente de l'Attrition",
  description: "Anticipez les départs de vos employés grâce à l'IA. Solution éthique et humaine pour le bien-être au travail.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body className={`${inter.className} antialiased`}>
        <PredictionProvider>
          {children}
          <ChatAssistant />
        </PredictionProvider>
      </body>
    </html>
  );
}
