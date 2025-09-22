
{-# LANGUAGE MagicHash #-}

module Hello.World where

import Data.List

-- Line comment
{- Block comment start
   {- nested deeper -}
-}

main :: IO ()                     -- 1: main, 11: ::
main = do                         -- 2: "do"
    let name = "Hackerman"        -- 2: let, 1: name, 4: string
        age  = 42                 -- 1: age, 3: number
        char = 'Z'                -- 1: char, 5: character
    putStrLn ("Hello, " ++ name) -- 11: ++
    print (age + 1)              -- 3: number, 11: +

> This is a literate comment       -- 21: Literate comment (Bird-style)
\begin{code}                      -- 22: Literate code delim
double x = x * 2                  -- 1: identifier, 11: operator
\end{code}                        -- 22: End literate code