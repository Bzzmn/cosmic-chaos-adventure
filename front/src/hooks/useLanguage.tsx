import { useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { useQueryClient } from '@tanstack/react-query';

export interface LanguageOption {
  code: string;
  name: string;
  nativeName: string;
  flag?: string;
}

// Supported languages
export const SUPPORTED_LANGUAGES: LanguageOption[] = [
  {
    code: 'en',
    name: 'English',
    nativeName: 'English',
    flag: '🇺🇸'
  },
  {
    code: 'es',
    name: 'Spanish',
    nativeName: 'Español',
    flag: '🇪🇸'
  }
];

/**
 * Custom hook for language management
 * Provides functions to change language and get current language information
 */
export const useLanguage = () => {
  const { i18n } = useTranslation();
  const queryClient = useQueryClient();
  
  const currentLanguageCode = i18n.language || 'en';
  
  // Get current language information
  const currentLanguage = SUPPORTED_LANGUAGES.find(
    lang => lang.code === currentLanguageCode
  ) || SUPPORTED_LANGUAGES[0];

  /**
   * Change the application language
   * @param languageCode - Language code to change to
   */
  const changeLanguage = useCallback((languageCode: string) => {
    if (languageCode !== currentLanguageCode) {
      // Change i18next language
      i18n.changeLanguage(languageCode);
      
      // Store the language preference in localStorage
      localStorage.setItem('language', languageCode);
      
      // Invalidate any language-dependent queries
      // This will force a refetch of data in the new language
      queryClient.invalidateQueries({ 
        predicate: (query) => {
          const queryKey = query.queryKey;
          // Check if the query has the language as part of its key
          return Array.isArray(queryKey) && 
            queryKey.length > 1 && 
            queryKey.includes(currentLanguageCode);
        }
      });
    }
  }, [i18n, currentLanguageCode, queryClient]);

  return {
    currentLanguage,
    currentLanguageCode,
    changeLanguage,
    languages: SUPPORTED_LANGUAGES
  };
};

 