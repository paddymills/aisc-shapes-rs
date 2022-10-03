
pub struct Shape {
    pub shape: String,
    pub edi_nomenclature: String,
    pub aisc_label: String,
}

impl Shape {
    pub fn new() -> Self {
        Self {
            shape: "W".into(),
            edi_nomenclature: "W12X64".into(),
            aisc_label: "W12X64".into()
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn new_design() {
        let result = Shape::new();
        assert_eq!(&result.shape, "W");
    }
}
