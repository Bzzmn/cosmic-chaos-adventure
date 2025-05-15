# Internationalization (i18n) Guidelines

This document provides guidelines for adding internationalization support to new components and features in the Cosmic Chaos Adventure application.

## General Principles

1. All user-facing text should be internationalized
2. Use translation keys that follow a hierarchical namespace pattern
3. Keep translations organized in the appropriate namespace files
4. Use variables for dynamic content rather than string concatenation
5. Always provide translations for all supported languages

## Adding Text to a Component

When adding text to a component, always use the translation function:

```jsx
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();
  
  return (
    <div>
      <h1>{t('myComponent.title')}</h1>
      <p>{t('myComponent.description')}</p>
    </div>
  );
}
```

## Using Namespaces

For larger components or specific feature areas, use namespaces to organize translations:

```jsx
import { useTranslation } from 'react-i18next';

function CharacterStats() {
  const { t } = useTranslation('character');
  
  return (
    <div>
      <h2>{t('stats.title')}</h2>
      <ul>
        <li>{t('stats.quantum_charisma')}: 85</li>
        <li>{t('stats.absurdity_resistance')}: 70</li>
      </ul>
    </div>
  );
}
```

## Variable Substitution

Use variables in translations for dynamic content:

```jsx
// In your translation file
// "greeting": "Hello, {{name}}!"

import { useTranslation } from 'react-i18next';

function Greeting({ name }) {
  const { t } = useTranslation();
  
  return <p>{t('greeting', { name })}</p>;
}
```

## HTML in Translations

For translations containing HTML markup, use the `TranslatedHTML` component:

```jsx
// In your translation file
// "message": "Click <span class='highlight'>here</span> to continue"

import TranslatedHTML from '@/components/TranslatedHTML';

function Message() {
  return <TranslatedHTML i18nKey="message" className="my-message" />;
}
```

## Date and Number Formatting

Use the i18n helpers for formatting dates and numbers according to the user's language:

```jsx
import { formatDateForLanguage, formatNumberForLanguage } from '@/lib/api/helpers';

function DateDisplay({ date, value }) {
  return (
    <div>
      <p>Date: {formatDateForLanguage(date)}</p>
      <p>Value: {formatNumberForLanguage(value)}</p>
    </div>
  );
}
```

## Adding a New Translation

1. Add the translation key to all language files:

```json
// src/locales/en/translation.json
{
  "newFeature": {
    "title": "New Feature",
    "description": "This is a new feature"
  }
}

// src/locales/es/translation.json
{
  "newFeature": {
    "title": "Nueva Funcionalidad",
    "description": "Esta es una nueva funcionalidad"
  }
}
```

## Adding a New Language

To add a new language:

1. Create a new folder in `src/locales` for the language (e.g., `fr` for French)
2. Copy all JSON files from an existing language folder
3. Translate all strings in the JSON files
4. Add the language to the `SUPPORTED_LANGUAGES` array in `src/hooks/useLanguage.tsx`

## API Requests with Language

When making API requests that need language information:

```jsx
import { getCurrentLanguage, addLanguageParam } from '@/lib/api/helpers';

// For GET requests with query parameters
const url = addLanguageParam('/api/data');  // Results in /api/data?lang=en

// For POST requests with language in the body
const body = {
  ...data,
  language: getCurrentLanguage()
};
```

## Testing Translations

To test translations:

1. Switch the language using the language switcher in the header
2. Verify that all text is correctly translated
3. Check that dynamic content (dates, numbers, interpolated variables) is properly formatted
4. Ensure that API requests are made with the correct language parameter

## Common Issues and Solutions

1. **Missing translation**: If a translation key is missing, i18next will fall back to the key name. Check the console for warnings about missing translations.

2. **HTML not rendering**: Make sure you're using the `TranslatedHTML` component for text containing HTML.

3. **Wrong language in API requests**: Ensure you're using the i18n helpers for API requests.

4. **Text not updating on language change**: Make sure your component re-renders when the language changes.

## Resources

- [i18next Documentation](https://www.i18next.com/overview/introduction)
- [react-i18next Documentation](https://react.i18next.com/) 