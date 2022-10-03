

pub mod units {
    // see https://play.rust-lang.org/?version=stable&mode=debug&edition=2018&gist=4ee51938ace195537df24613b3c54564
    use std::sync::atomic::{AtomicBool, Ordering};

    static METRIC: AtomicBool = AtomicBool::new(false);

    pub fn metric() {
        METRIC.store(true, Ordering::Relaxed);
    }
    
    pub fn english() {
        METRIC.store(false, Ordering::Relaxed);
    }
}


#[cfg_attr(feature = "design", path="design/shape.rs")]
mod shape;

pub use shape::Shape;


// #[cfg(test)]
// mod tests {
//     use super::*;

//     #[test]
//     #[cfg(feature="design")]
//     fn new_design() {
//         let result = Shape::new();
//         assert_eq!(result, 1);
//     }
    
//     #[test]
//     #[cfg(not(feature="design"))]
//     fn new_design() {
//         let result = Shape::new();
//         assert_eq!(result, 2);
//     }
// }
