# Internationalization (i18n) in Cosmic Chaos Adventure

This directory contains translations for the Cosmic Chaos Adventure application. The project uses [i18next](https://www.i18next.com/) and [react-i18next](https://react.i18next.com/) for internationalization.

## Structure

Translations are organized by language and namespace:

```
locales/
├── en/                     # English translations
│   ├── translation.json    # General translations
│   ├── character.json      # Character-related translations
│   ├── adventure.json      # Adventure-related translations
│   └── ...                 # Other namespaces
├── es/                     # Spanish translations
│   ├── translation.json
│   ├── character.json
│   ├── adventure.json
│   └── ...
└── ...                     # Other languages
```

## Translation Namespaces

The translations are divided into several namespaces to better organize them:

- `translation`: General translations used across the application (default namespace)
- `character`: Translations related to character creation, details, and management
- `adventure`: Translations related to adventures, stories, and game progress

## Usage

### Basic Translation

```jsx
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();
  
  return <p>{t('common.loading')}</p>;
}
```

### Using Namespaces

```jsx
import { useTranslation } from 'react-i18next';

function CharacterComponent() {
  const { t } = useTranslation('character');
  
  return <p>{t('stats.quantum_charisma')}</p>;
}
```

### Translations with Variables

```jsx
import { useTranslation } from 'react-i18next';

function ProgressComponent({ goal }) {
  const { t } = useTranslation('adventure');
  
  return <p>{t('progress.nextUpdate', { goal })}</p>;
}
```

### HTML Content in Translations

Use the `TranslatedHTML` component for translations containing HTML:

```jsx
import TranslatedHTML from '@/components/TranslatedHTML';

function StrikeMessage({ goal }) {
  return (
    <TranslatedHTML 
      i18nKey="adventure.progress.description" 
      values={{ goal }} 
    />
  );
}
```

## Adding a New Language

1. Create a new directory in `locales/` for your language (e.g., `fr/` for French)
2. Copy all JSON files from an existing language (e.g., `en/`) to the new language directory
3. Translate all strings in the copied JSON files
4. Add the new language to the language switcher in `src/components/LanguageSwitcher.tsx`
5. Update the resources in `src/lib/i18n.ts` to include the new language

## Best Practices

1. Use translation keys that reflect the component and purpose of the text
2. Group related translations together in the same namespace
3. Keep translations simple and avoid complex nested structures
4. Use variables for dynamic content rather than concatenating strings
5. Use the `TranslatedHTML` component for translations containing HTML 