'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

// Animation variants
const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2
    }
  }
};

const scaleIn = {
  hidden: { scale: 0.8, opacity: 0 },
  visible: { scale: 1, opacity: 1, transition: { duration: 0.5 } }
};

export default function Home() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="min-h-screen bg-dark text-light selection:bg-emerald selection:text-white overflow-hidden">

      {/* Background Animated Elements */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-emerald/10 rounded-full blur-[100px] animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-emerald-dark/10 rounded-full blur-[100px] animate-pulse delay-700" />
      </div>

      {/* Navigation */}
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
        className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrolled ? 'bg-dark/90 backdrop-blur-md border-b border-emerald/20 py-4 shadow-lg' : 'bg-transparent py-6'
          }`}
      >
        <div className="max-w-7xl mx-auto px-6 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-emerald to-emerald-light bg-clip-text text-transparent hover:scale-105 transition-transform">
            AttritionAI
          </Link>
          <div className="flex gap-8 items-center">
            <a href="#features" className="text-light/80 hover:text-emerald-light transition-colors font-medium">
              Fonctionnalités
            </a>
            <a href="#ethics" className="text-light/80 hover:text-emerald-light transition-colors font-medium">
              Éthique
            </a>
            <Link
              href="/prediction"
              className="px-6 py-2.5 bg-gradient-to-r from-emerald to-emerald-dark rounded-full font-semibold text-white shadow-lg shadow-emerald/20 hover:shadow-emerald/40 hover:-translate-y-0.5 transition-all"
            >
              Essayer Maintenant →
            </Link>
          </div>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <section className="relative pt-40 pb-20 px-6 z-10">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={staggerContainer}
          className="max-w-7xl mx-auto text-center"
        >
          <motion.div variants={fadeInUp} className="inline-block px-4 py-2 bg-emerald/10 border border-emerald/30 rounded-full text-emerald-light text-sm font-semibold mb-8 backdrop-blur-sm">
            🌱 IA Éthique & Bien-être au Travail
          </motion.div>

          <motion.h1 variants={fadeInUp} className="text-6xl md:text-8xl font-bold mb-8 leading-tight tracking-tight">
            Prédisez l'Attrition avec<br />
            <span className="bg-gradient-to-r from-emerald via-emerald-light to-emerald bg-clip-text text-transparent animate-gradient-x">
              Humanité & Intelligence
            </span>
          </motion.h1>

          <motion.p variants={fadeInUp} className="text-xl md:text-2xl text-light/70 max-w-3xl mx-auto mb-12 leading-relaxed font-light">
            Anticipez les départs de vos employés grâce à notre modèle d'IA éthique.
            Analysez 29 indicateurs de bien-être et obtenez des recommandations humaines.
          </motion.p>

          <motion.div variants={fadeInUp} className="flex gap-6 justify-center flex-wrap">
            <Link
              href="/prediction"
              className="group relative px-8 py-4 bg-emerald rounded-xl font-bold text-lg text-white overflow-hidden shadow-2xl shadow-emerald/30 transition-all hover:scale-105"
            >
              <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-shimmer" />
              <span className="relative flex items-center gap-2">
                🚀 Commencer Gratuitement
              </span>
            </Link>
            <a
              href="#features"
              className="px-8 py-4 bg-white/5 border border-white/10 rounded-xl font-semibold text-lg hover:bg-white/10 hover:border-emerald/30 transition-all backdrop-blur-sm"
            >
              En savoir plus
            </a>
          </motion.div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-32 px-6 bg-dark-light/30 relative overflow-hidden">
        <div className="max-w-7xl mx-auto relative z-10">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeInUp}
            className="text-center mb-20"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Fonctionnalités Clés</h2>
            <p className="text-light/60 text-xl font-light">Une approche humaine de la prédiction d'attrition</p>
          </motion.div>

          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={staggerContainer}
            className="grid md:grid-cols-3 gap-8"
          >
            {[
              { icon: "🤖", title: "IA Éthique", desc: "Modèle RandomForest transparent et explicable, respectueux de la vie privée." },
              { icon: "💚", title: "Bien-être RH", desc: "Focus sur le bien-être avec recommandations pour améliorer la QVT." },
              { icon: "📊", title: "29 Indicateurs", desc: "Analyse complète : RH, satisfaction, performance et données temporelles." },
              { icon: "⚡", title: "Temps Réel", desc: "Résultats instantanés avec probabilités détaillées pour action rapide." },
              { icon: "🎯", title: "Recommandations", desc: "Actions concrètes et humaines pour retenir vos talents." },
              { icon: "🔒", title: "Confidentialité", desc: "Données privées traitées localement sur votre infrastructure sécurisée." }
            ].map((feature, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                whileHover={{ y: -10, transition: { duration: 0.2 } }}
                className="p-8 bg-dark/50 border border-emerald/10 rounded-3xl hover:border-emerald/40 hover:bg-dark-light/80 transition-all group backdrop-blur-sm shadow-lg hover:shadow-emerald/10"
              >
                <div className="text-5xl mb-6 bg-dark-light w-20 h-20 flex items-center justify-center rounded-2xl group-hover:scale-110 transition-transform">{feature.icon}</div>
                <h3 className="text-2xl font-bold mb-4 group-hover:text-emerald-light transition-colors">{feature.title}</h3>
                <p className="text-light/60 leading-relaxed group-hover:text-light/80 transition-colors">
                  {feature.desc}
                </p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Ethics Section */}
      <section id="ethics" className="py-32 px-6 relative">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-7xl mx-auto"
        >
          <div className="relative bg-gradient-to-br from-emerald/10 to-dark p-1 rounded-[3rem]">
            <div className="absolute inset-0 bg-emerald/20 blur-3xl -z-10" />
            <div className="bg-dark/90 backdrop-blur-xl border border-emerald/20 rounded-[2.9rem] p-12 md:p-20 overflow-hidden relative">

              {/* Decorative circle */}
              <div className="absolute top-0 right-0 w-64 h-64 bg-emerald/10 rounded-full blur-[80px]" />

              <div className="relative z-10">
                <div className="text-center mb-16">
                  <h2 className="text-4xl md:text-5xl font-bold mb-6">Éthique & Transparence</h2>
                  <p className="text-light/60 text-xl">Notre engagement pour une IA responsable</p>
                </div>

                <div className="grid md:grid-cols-2 gap-12">
                  {[
                    { title: "Transparence Totale", desc: "Modèle explicable pour comprendre chaque prédiction." },
                    { title: "Respect de la Vie Privée", desc: "Données anonymisées et traitement local uniquement." },
                    { title: "Approche Humaine", desc: "L'IA assiste les RH, elle ne remplace pas l'humain." },
                    { title: "Pas de Discrimination", desc: "Modèle entraîné pour éviter les biais et garantir l'équité." }
                  ].map((item, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: i % 2 === 0 ? -20 : 20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: i * 0.1 }}
                      className="flex gap-6 items-start group"
                    >
                      <div className="flex-shrink-0 w-12 h-12 rounded-full bg-emerald/10 flex items-center justify-center border border-emerald/20 group-hover:bg-emerald/20 transition-colors">
                        <span className="text-xl">✅</span>
                      </div>
                      <div>
                        <h3 className="text-xl font-bold mb-2 text-emerald-light group-hover:text-emerald transition-colors">{item.title}</h3>
                        <p className="text-light/60 group-hover:text-light/80 transition-colors">{item.desc}</p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-6 bg-dark-light/30 border-y border-white/5">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={staggerContainer}
            className="grid md:grid-cols-4 gap-12 text-center"
          >
            {[
              { val: "95%", label: "Précision du Modèle" },
              { val: "29", label: "Features Analysées" },
              { val: "<1s", label: "Temps de Prédiction" },
              { val: "100%", label: "Éthique & Transparent" }
            ].map((stat, i) => (
              <motion.div key={i} variants={scaleIn} className="group cursor-default">
                <div className="text-6xl font-bold bg-gradient-to-r from-emerald to-emerald-light bg-clip-text text-transparent mb-4 group-hover:scale-110 transition-transform duration-300 inline-block">
                  {stat.val}
                </div>
                <p className="text-light/50 font-medium tracking-wide uppercase text-sm group-hover:text-light/80 transition-colors">{stat.label}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32 px-6">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-4xl mx-auto text-center relative"
        >
          {/* Glow effect */}
          <div className="absolute inset-0 bg-emerald/20 blur-[100px] rounded-full -z-10" />

          <div className="p-12 border border-emerald/30 rounded-[2.5rem] bg-dark/50 backdrop-blur-xl relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-b from-emerald/10 to-transparent opacity-50" />

            <div className="relative z-10">
              <h2 className="text-4xl md:text-5xl font-bold mb-6">Prêt à Améliorer le Bien-être ?</h2>
              <p className="text-light/70 text-xl mb-10 max-w-2xl mx-auto">
                Rejoignez les entreprises qui utilisent l'IA éthique pour retenir leurs talents.
              </p>
              <Link
                href="/prediction"
                className="inline-block px-12 py-5 bg-gradient-to-r from-emerald to-emerald-dark rounded-full font-bold text-xl text-white shadow-xl shadow-emerald/30 hover:shadow-emerald/50 hover:-translate-y-1 hover:scale-105 transition-all duration-300"
              >
                🎯 Lancer une Prédiction
              </Link>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-emerald/10 bg-dark-light/20">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-light/40 mb-4 font-medium">© 2024 AttritionAI - IA Éthique pour le Bien-être au Travail</p>
          <div className="flex justify-center gap-6 text-sm text-light/30">
            <span className="hover:text-emerald cursor-pointer transition-colors">Mentions Légales</span>
            <span className="hover:text-emerald cursor-pointer transition-colors">Confidentialité</span>
            <span className="hover:text-emerald cursor-pointer transition-colors">Contact</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
