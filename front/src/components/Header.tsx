import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from 'react-i18next';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { User, Settings, LogOut } from 'lucide-react';
import NeonTitle from './NeonTitle';
import LanguageSwitcher from './LanguageSwitcher';

const Header: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const { t } = useTranslation();
  
  return (
    <header className="fixed top-0 left-0 right-0 z-50 p-4 ">
      <div className="container mx-auto flex justify-end items-center">
        
        <div className="flex items-center space-x-4">
          <LanguageSwitcher />
          
          {isAuthenticated ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm" className="rounded-full w-10 h-10 p-0 bg-cosmic-dark/60">
                  <Avatar className="h-9 w-9 border-2 border-cosmic-cyan">
                    <AvatarFallback className="bg-cosmic-dark text-cosmic-cyan">
                      {user?.name?.charAt(0) || user?.email?.charAt(0) || 'U'}
                    </AvatarFallback>
                    {user?.image_url && <AvatarImage src={user.image_url} alt={user.name || ''} />}
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56 bg-cosmic-dark border border-cosmic-cyan/30">
                <DropdownMenuLabel className="text-cosmic-cyan">
                  {user?.name || user?.email}
                </DropdownMenuLabel>
                <DropdownMenuSeparator className="bg-cosmic-cyan/20" />
                <DropdownMenuItem asChild>
                  <Link to="/my-creatures" className="flex cursor-pointer items-center">
                    <User className="mr-2 h-4 w-4" />
                    <span>{t('header.character')}</span>
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link to="/settings" className="flex cursor-pointer items-center">
                    <Settings className="mr-2 h-4 w-4" />
                    <span>{t('common.settings', 'Settings')}</span>
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuSeparator className="bg-cosmic-cyan/20" />
                <DropdownMenuItem 
                  className="flex cursor-pointer items-center text-red-500 focus:text-red-500"
                  onClick={logout}
                >
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>{t('common.logout')}</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <Link to="/auth">
              <Button variant="outline" size="sm" className="border-cosmic-cyan/50 text-cosmic-cyan hover:bg-cosmic-cyan/10">
                {t('common.login')}
              </Button>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
