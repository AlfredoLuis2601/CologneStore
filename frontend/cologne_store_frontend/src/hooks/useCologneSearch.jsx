import { useState } from 'react';
import { useNavigate } from 'react-router';
import { getCologneByName } from '../services/cologneService.js'; 

export function useCologneSearch() {
  const [cologneSearch, setCologneSearch] = useState('');
  const [searchError, setSearchError] = useState(null);
  const navigate = useNavigate();

  const handleSearch = async (term) => {
    setCologneSearch(term);
    try {
      setSearchError(null);    
      const result = await getCologneByName(term);
      navigate(`/colognedetails/${result.uid}`);
      
    } catch (error) {
      setSearchError({
        code: error?.code,
        message: error.message,
        variant: error?.category
      });
    } 
  };

  return {
    cologneSearch,
    setCologneSearch,
    searchError,
    handleSearch
  };
}