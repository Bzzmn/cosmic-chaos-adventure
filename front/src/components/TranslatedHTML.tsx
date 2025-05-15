import React from 'react';
import { useTranslation } from 'react-i18next';

interface TranslatedHTMLProps {
  i18nKey: string;
  values?: Record<string, string | number>;
  className?: string;
}

/**
 * Componente que permite renderizar traducciones que contienen HTML usando interpolación
 * y dangerouslySetInnerHTML para permitir HTML en las traducciones
 * 
 * Ejemplo de uso:
 * <TranslatedHTML i18nKey="landing.strikeMessage" values={{ goal: 1000 }} />
 */
const TranslatedHTML: React.FC<TranslatedHTMLProps> = ({ 
  i18nKey, 
  values = {}, 
  className = ''
}) => {
  const { t } = useTranslation();

  return (
    <div 
      className={className}
      dangerouslySetInnerHTML={{ 
        __html: t(i18nKey, { ...values, interpolation: { escapeValue: false } }) 
      }} 
    />
  );
};

export default TranslatedHTML; 