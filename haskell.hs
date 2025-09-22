
{-# LANGUAGE MagicHash #-}

module Hello.World where

import Data.List

-- Line comment
{- Block comment start
   {- nested deeper -}
-}

main :: IO ()
main = do
    let name = "Hackerman"
        age  = 42
        char = 'Z'
    putStrLn ("Hello, " ++ name)
    print (age + 1)
